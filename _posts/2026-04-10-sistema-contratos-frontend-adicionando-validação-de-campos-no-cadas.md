---
layout: post
title: "Adicionando Validação de Campos no Cadastro da Instituição"
date: 2026-04-10 17:30:22 +0000
categories: [Frontend]
tags: ["feature", "React", "Sistema Contratos Frontend", "TypeScript"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

## O que foi feito

No commit `e2fb77c`, adicionamos validação de campos no cadastro da instituição no repositório Sistema-Contratos-Frontend. Os arquivos alterados incluem `.gitignore`, `NovaInstituicaoForm.tsx` e `EditarCadastroTab.tsx`. 

No arquivo `NovaInstituicaoForm.tsx`, removemos a importação do componente `Calendar` e adicionamos funcionalidades para validação de campos, como e-mail e CPF/CNPJ. Além disso, implementamos a exibição de erros de forma mais amigável ao usuário, utilizando o hook `useToast` para exibir mensagens de erro.

```tsx
const NovaInstituicaoForm = () => {
  // ...
  const { showToast } = useToast();
  // ...
  const showToast(
    e instanceof Error ? e.message : "Erro ao carregar portes de empresa",
    "error",
  );
  // ...
}
```

No arquivo `.gitignore`, removemos a linha que ignorava o diretório `app/(protected)/contratos/gerenciar/fiscalizar/*`.

## Por que foi feito

Essas mudanças foram feitas para melhorar a experiência do usuário e evitar erros durante o cadastro de instituições. A validação de campos ajuda a garantir que os dados sejam consistentes e corretos, evitando problemas futuros. Além disso, a exibição de erros de forma mais amigável ao usuário melhora a usabilidade do sistema.

A remoção do componente `Calendar` pode ter sido feita para simplificar a interface do usuário e evitar a utilização de componentes desnecessários.

## Impacto

Com essas mudanças, o usuário final perceberá uma melhoria na usabilidade do sistema, pois os erros serão exibidos de forma mais clara e amigável. Além disso, a validação de campos ajuda a garantir que os dados sejam consistentes e corretos, evitando problemas futuros.

No entanto, é importante notar que a remoção do componente `Calendar` pode afetar funcionalidades que dependiam desse componente. Portanto, é importante testar o sistema após essas mudanças para garantir que tudo esteja funcionando corretamente.

Essas mudanças também podem afetar a performance do sistema, pois a validação de campos e a exibição de erros podem adicionar um pouco de carga ao sistema. No entanto, essas mudanças são necessárias para melhorar a usabilidade e evitar erros.

---
*Post gerado automaticamente a partir dos commits [`e2fb77c`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/e2fb77c79b468b66a823f5b095ebd6478f3806d3) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*