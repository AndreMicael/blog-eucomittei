#!/usr/bin/env python3
"""
Gera posts Jekyll automaticamente a partir de commits do GitHub.
Usa Gemini 1.5 Flash para criar os textos dos posts.
"""

import os
import json
import re
import sys
from datetime import datetime, timezone, timedelta
from pathlib import Path

import requests
import yaml
from groq import Groq


def load_config():
    config_path = Path(__file__).parent.parent / "config.yml"
    with open(config_path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


def load_last_processed():
    path = Path(__file__).parent.parent / "last_processed.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        # Migra formato antigo {repo: "sha"} para novo {repo: {last_sha, processed: []}}
        for key, value in data.items():
            if isinstance(value, str):
                data[key] = {"last_sha": value, "processed": [value]}
        return data
    return {}


def save_last_processed(data):
    path = Path(__file__).parent.parent / "last_processed.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def is_already_processed(repo_key, sha, last_processed):
    """Verifica se um SHA já foi processado anteriormente."""
    repo_data = last_processed.get(repo_key, {})
    if isinstance(repo_data, str):
        return repo_data == sha
    return sha in repo_data.get("processed", [])


def mark_as_processed(repo_key, sha, last_processed):
    """Registra o SHA como processado, mantendo histórico dos últimos 200."""
    if repo_key not in last_processed:
        last_processed[repo_key] = {"last_sha": sha, "processed": []}
    repo_data = last_processed[repo_key]
    repo_data["last_sha"] = sha
    if sha not in repo_data["processed"]:
        repo_data["processed"].append(sha)
    # Limita histórico para não crescer demais
    repo_data["processed"] = repo_data["processed"][-200:]


def github_get(url, github_token, params=None, accept=None):
    headers = {"Authorization": f"token {github_token}"}
    if accept:
        headers["Accept"] = accept
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response


def get_new_commits(owner, repo, last_processed_data, github_token):
    """Retorna commits não processados ainda para este repo."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = github_get(url, github_token, params={"per_page": 30})
    commits = response.json()

    if not commits:
        return []

    repo_key = f"{owner}/{repo}"
    repo_data = last_processed_data.get(repo_key, {})
    last_sha = repo_data.get("last_sha") if isinstance(repo_data, dict) else repo_data
    processed_set = set(repo_data.get("processed", [])) if isinstance(repo_data, dict) else {repo_data}

    # Primeira execução: processa só o commit mais recente
    if not last_sha:
        return commits[:1]

    # Coleta commits novos (antes de encontrar o last_sha)
    new_commits = []
    for commit in commits:
        if commit["sha"] == last_sha:
            break
        new_commits.append(commit)

    # Filtra qualquer SHA que já esteja no histórico (segurança extra)
    new_commits = [c for c in new_commits if c["sha"] not in processed_set]

    return new_commits


def get_commit_details(owner, repo, sha, github_token):
    """Retorna detalhes do commit incluindo diff."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits/{sha}"

    # Busca detalhes com lista de arquivos
    detail = github_get(url, github_token).json()

    # Busca diff em texto
    diff_text = github_get(
        url, github_token, accept="application/vnd.github.v3.diff"
    ).text

    return detail, diff_text[:6000]  # Limita diff para não estourar tokens


def build_prompt(commits_data, language, repo_name, repo_url):
    """Monta o prompt para o Gemini com todos os commits do dia."""
    commits_summary = []
    for i, (commit, detail, _) in enumerate(commits_data, 1):
        sha = commit["sha"][:7]
        message = commit["commit"]["message"]
        author = commit["commit"]["author"]["name"]
        date = commit["commit"]["author"]["date"]
        files_changed = [f["filename"] for f in detail.get("files", [])][:10]

        commits_summary.append(
            f"**Commit {i}** (`{sha}`):\n"
            f"- Mensagem: {message}\n"
            f"- Autor: {author}\n"
            f"- Data: {date}\n"
            f"- Arquivos: {', '.join(files_changed) if files_changed else 'N/A'}"
        )

    # Usa o diff do commit mais recente para contexto de código
    latest_diff = commits_data[0][2] if commits_data else ""

    commits_text = "\n\n".join(commits_summary)

    return f"""Você é um escritor técnico de blog de desenvolvimento de software.
Com base nos commits abaixo do repositório "{repo_name}", escreva um post de blog em {language}.

REGRAS:
- Escreva em tom técnico mas acessível
- Explique O QUE foi feito e POR QUE (infira o motivo pelo contexto)
- Entre 300 e 500 palavras de conteúdo
- Use Markdown com subtítulos (##), listas e destaque de código quando relevante
- NÃO inclua frontmatter YAML (---) — só o conteúdo
- A PRIMEIRA LINHA deve ser um título com H1 (# Título aqui)
- Não seja genérico: mencione especificamente o que mudou

REPOSITÓRIO: {repo_name}
URL: {repo_url}

COMMITS:
{commits_text}

DIFF DO COMMIT MAIS RECENTE (para contexto):
```
{latest_diff}
```

Escreva o post:"""


def generate_post_content(commits_data, language, repo_name, repo_url, groq_api_key):
    """Chama Groq para gerar o post."""
    client = Groq(api_key=groq_api_key)

    prompt = build_prompt(commits_data, language, repo_name, repo_url)

    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=1024,
    )
    return response.choices[0].message.content.strip()


def slugify(text):
    """Converte texto em slug para nome de arquivo."""
    text = text.lower()
    text = re.sub(r"[^\w\s-]", "", text)
    text = re.sub(r"[\s_]+", "-", text)
    text = text.strip("-")
    return text[:60]


def detect_categories_and_tags(repo_name, commits_data):
    """Detecta categorias e tags a partir do nome do repo e arquivos alterados."""
    all_files = []
    for _, detail, _ in commits_data:
        all_files += [f["filename"] for f in detail.get("files", [])]

    all_files_str = " ".join(all_files).lower()
    messages = " ".join(
        c[0]["commit"]["message"].lower() for c in commits_data
    )

    # Categoria principal baseada no repo
    repo_lower = repo_name.lower()
    if "frontend" in repo_lower or "front" in repo_lower:
        category = "Frontend"
    elif "backend" in repo_lower or "back" in repo_lower or "api" in repo_lower:
        category = "Backend"
    elif "mobile" in repo_lower or "app" in repo_lower:
        category = "Mobile"
    elif "infra" in repo_lower or "devops" in repo_lower or "deploy" in repo_lower:
        category = "DevOps"
    else:
        category = "Desenvolvimento"

    # Tags baseadas em arquivos e mensagens de commit
    tags = set()
    tags.add(repo_name.replace("-", " "))

    tag_rules = {
        "React": [".jsx", ".tsx", "react", "component"],
        "Vue": [".vue", "vuex", "nuxt"],
        "Angular": ["angular", ".component.ts"],
        "TypeScript": [".ts", ".tsx", "typescript"],
        "JavaScript": [".js", ".jsx", "javascript"],
        "Python": [".py", "python", "django", "flask", "fastapi"],
        "Java": [".java", "spring", "maven", "gradle"],
        "Docker": ["dockerfile", "docker-compose", "container"],
        "CI/CD": [".github/workflows", ".gitlab-ci", "pipeline"],
        "banco de dados": [".sql", "migration", "model", "schema", "database"],
        "API": ["api", "endpoint", "route", "controller", "swagger"],
        "testes": ["test", "spec", ".test.", ".spec.", "jest", "pytest"],
        "autenticação": ["auth", "login", "jwt", "token", "oauth"],
        "UI": [".css", ".scss", ".sass", "style", "layout", "component"],
        "bugfix": ["fix", "bug", "correção", "corrig"],
        "feature": ["feat", "nova", "new feature", "adiciona", "implement"],
        "refatoração": ["refactor", "refatora", "cleanup", "clean up"],
        "documentação": ["docs", "readme", "documentation", ".md"],
    }

    combined = all_files_str + " " + messages
    for tag, keywords in tag_rules.items():
        if any(kw in combined for kw in keywords):
            tags.add(tag)

    # Limita a 6 tags para não poluir
    tag_list = list(tags)[:6]

    return category, tag_list


def write_jekyll_post(content, repo_name, repo_url, commits_data):
    """Escreve o arquivo .md no formato Jekyll em _posts/."""
    lines = content.strip().split("\n")

    # Extrai título do H1 gerado pela IA
    post_title = f"Atualização em {repo_name}"
    body_lines = lines
    if lines and lines[0].startswith("# "):
        post_title = lines[0][2:].strip()
        body_lines = lines[1:]

    body = "\n".join(body_lines).strip()

    # Data do commit mais recente
    latest_date_str = commits_data[0][0]["commit"]["author"]["date"]
    latest_date = datetime.fromisoformat(latest_date_str.replace("Z", "+00:00"))
    date_for_file = latest_date.strftime("%Y-%m-%d")
    date_for_frontmatter = latest_date.strftime("%Y-%m-%d %H:%M:%S %z")

    # Links dos commits
    commit_links = []
    for commit, _, _ in commits_data:
        sha = commit["sha"]
        short_sha = sha[:7]
        commit_links.append(f"[`{short_sha}`]({repo_url}/commit/{sha})")

    links_text = ", ".join(commit_links)

    # Categorias e tags inteligentes
    category, tags = detect_categories_and_tags(repo_name, commits_data)

    safe_title = post_title.replace('"', "'")
    filename = f"{date_for_file}-{slugify(repo_name)}-{slugify(post_title)[:40]}.md"

    frontmatter = f"""---
layout: post
title: "{safe_title}"
date: {date_for_frontmatter}
categories: [{category}]
tags: {json.dumps(tags, ensure_ascii=False)}
repo: "{repo_url}"
---

"""

    footer = f"\n\n---\n*Post gerado automaticamente a partir dos commits {links_text} em [{repo_name}]({repo_url})*"

    full_content = frontmatter + body + footer

    posts_dir = Path(__file__).parent.parent / "_posts"
    posts_dir.mkdir(exist_ok=True)

    post_path = posts_dir / filename
    with open(post_path, "w", encoding="utf-8") as f:
        f.write(full_content)

    return filename


def main():
    github_token = os.environ.get("GITHUB_TOKEN")
    groq_api_key = os.environ.get("GROQ_API_KEY")

    if not github_token:
        print("ERRO: variável GITHUB_TOKEN não definida", file=sys.stderr)
        sys.exit(1)
    if not groq_api_key:
        print("ERRO: variável GROQ_API_KEY não definida", file=sys.stderr)
        sys.exit(1)

    config = load_config()
    last_processed = load_last_processed()

    language = config.get("language", "português")
    repos = config.get("repos", [])
    max_commits_per_repo = config.get("max_commits_per_repo", 5)

    if not repos:
        print("Nenhum repositório configurado em config.yml")
        sys.exit(0)

    generated_posts = []

    for repo_config in repos:
        owner = repo_config["owner"]
        repo = repo_config["name"]
        repo_key = f"{owner}/{repo}"
        repo_url = f"https://github.com/{owner}/{repo}"

        print(f"\nProcessando {repo_key}...")

        try:
            new_commits = get_new_commits(owner, repo, last_processed, github_token)

            if not new_commits:
                print(f"  Nenhum commit novo em {repo_key} — pulando.")
                continue

            # Limita para evitar posts muito longos
            new_commits = new_commits[:max_commits_per_repo]
            print(f"  Encontrados {len(new_commits)} commit(s) novo(s)")

            # Busca detalhes de cada commit
            commits_data = []
            for commit in new_commits:
                sha = commit["sha"]
                print(f"  Buscando detalhes do commit {sha[:7]}...")
                detail, diff = get_commit_details(owner, repo, sha, github_token)
                commits_data.append((commit, detail, diff))

            # Gera post com Groq
            print(f"  Gerando post com Groq...")
            content = generate_post_content(
                commits_data, language, repo, repo_url, groq_api_key
            )

            # Escreve arquivo Jekyll
            filename = write_jekyll_post(content, repo, repo_url, commits_data)
            generated_posts.append(filename)
            print(f"  Post criado: {filename}")

            # Registra todos os SHAs processados no histórico
            for commit in new_commits:
                mark_as_processed(repo_key, commit["sha"], last_processed)

        except requests.HTTPError as e:
            print(f"  ERRO ao acessar GitHub para {repo_key}: {e}", file=sys.stderr)
        except Exception as e:
            print(f"  ERRO ao processar {repo_key}: {e}", file=sys.stderr)

    save_last_processed(last_processed)

    print(f"\n{'='*40}")
    if generated_posts:
        print(f"Posts gerados ({len(generated_posts)}):")
        for p in generated_posts:
            print(f"  - {p}")
    else:
        print("Nenhum post novo gerado.")


if __name__ == "__main__":
    main()
