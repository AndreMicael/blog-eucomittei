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
            return json.load(f)
    return {}


def save_last_processed(data):
    path = Path(__file__).parent.parent / "last_processed.json"
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)


def github_get(url, github_token, params=None, accept=None):
    headers = {"Authorization": f"token {github_token}"}
    if accept:
        headers["Accept"] = accept
    response = requests.get(url, headers=headers, params=params, timeout=30)
    response.raise_for_status()
    return response


def get_new_commits(owner, repo, since_sha, github_token):
    """Retorna commits novos desde since_sha (ou o último commit se não houver estado)."""
    url = f"https://api.github.com/repos/{owner}/{repo}/commits"
    response = github_get(url, github_token, params={"per_page": 30})
    commits = response.json()

    if not commits:
        return []

    if not since_sha:
        # Primeira execução: processa só o commit mais recente
        return commits[:1]

    new_commits = []
    for commit in commits:
        if commit["sha"] == since_sha:
            break
        new_commits.append(commit)

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


def write_jekyll_post(content, repo_name, repo_url, commits_data):
    """Escreve o arquivo .md no formato Jekyll em _posts/."""
    lines = content.strip().split("\n")

    # Extrai título do H1 gerado pelo Gemini
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
    tags = [repo_name.replace("-", " "), "desenvolvimento", "open source"]

    safe_title = post_title.replace('"', "'")
    filename = f"{date_for_file}-{slugify(repo_name)}-{slugify(post_title)[:40]}.md"

    frontmatter = f"""---
layout: post
title: "{safe_title}"
date: {date_for_frontmatter}
categories: [desenvolvimento, commits]
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
            since_sha = last_processed.get(repo_key)
            new_commits = get_new_commits(owner, repo, since_sha, github_token)

            if not new_commits:
                print(f"  Nenhum commit novo em {repo_key}")
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

            # Gera post com Gemini
            print(f"  Gerando post com Gemini...")
            content = generate_post_content(
                commits_data, language, repo, repo_url, groq_api_key
            )

            # Escreve arquivo Jekyll
            filename = write_jekyll_post(content, repo, repo_url, commits_data)
            generated_posts.append(filename)
            print(f"  Post criado: {filename}")

            # Atualiza estado com o commit mais recente
            last_processed[repo_key] = new_commits[0]["sha"]

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
