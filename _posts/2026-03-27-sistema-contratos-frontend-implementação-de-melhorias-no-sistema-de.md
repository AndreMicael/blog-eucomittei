---
layout: post
title: "Implementação de Melhorias no Sistema de Contratos do Frontend"
date: 2026-03-27 17:27:08 +0000
categories: [Frontend]
tags: ["UI", "Sistema Contratos Frontend", "JavaScript", "bugfix", "React", "feature"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

Este post detalha as mudanças realizadas no repositório "Sistema-Contratos-Frontend" com o objetivo de melhorar a experiência do usuário e corrigir problemas existentes. As melhorias abordam desde a refatoração de componentes até a implementação de novas funcionalidades, visando sempre aprimorar a usabilidade e a performance do sistema.

## O que foi feito

As principais mudanças incluem:

- **Refatoração do componente de inputs do Novo Contrato**: Foram realizadas melhorias na estrutura e no layout dos componentes de input para um melhor UX.
- **Correção de bug crítico no build**: Conflitos de dependências foram resolvidos, garantindo a estabilidade do sistema.
- **Adição do React Query para cache de fetch**: Melhoria na performance com a implementação do React Query para gerenciar requisições e cache de dados.
- **Puxando a vigência dos aditivos**: Implementação de lógica para calcular a vigência dos aditivos contratuais.
- **Remoção de campos mockup da licitação**: Remoção de dados mock para uma representação mais realista dos contratos.
- **Correções de erros de design**: Ajustes visuais para manter a consistência do design sistema.

### Detalhes Técnicos

Nos commits realizados, podemos observar as seguintes mudanças técnicas:

```diff
- const mockFinanceiro = {
-  valorOriginal:         108_000.00,
-  valorAtualizado:       118_800.00,
+ const mockFinanceiro = {
+  valorOriginal: 108_000.0,
+  valorAtualizado: 118_800.0,
```

A mudança acima ilustra a simplificação dos valores monetários, removendo o cents quando não aplicável.

```typescript
type ContratoAditivo = {
  id_contrato_aditivo: string;
  numero_aditivo: string | null;
  // ...
};

export function getFimVigencia(contrato: ContratoDetalhe): string | null {
  const ativosComData = (contrato.aditivos ?? []).filter(
    (a) => a.ativo && a.fim_vigencia,
  );
  // Lógica para determinar a vigência baseada nos aditivos
}
```

Essa porção do código introduz a tipagem para `ContratoAditivo` e uma função para calcular o fim da vigência com base nos aditivos do contrato.

## Por que foi feito

As mudanças foram motivadas por:

- **Melhoria da UX**: Com a refatoração de componentes e a correção de bugs, o sistema se torna mais amigável e fácil de usar.
- **Necessidade de escalabilidade**: A implementação do React Query ajuda a gerenciar melhor as requisições e o cache, preparando o sistema para crescer.
- **Correção de bugs**: Resolução de problemas técnicos para garantir a estabilidade e a confiabilidade do sistema.

## Impacto

O resultado prático dessas mudanças inclui:

- **Experiência do usuário melhorada**: Com componentes mais intuitivos e uma interface mais consistente, os usuários têm uma experiência mais agradável.
- **Performance aumentada**: O uso do React Query e a correção de bugs contribuem para um desempenho mais rápido e eficiente do sistema.
- **Preparação para novas funcionalidades**: Com a base técnica mais sólida, o sistema está pronto para incorporar novas features e melhorias futuras.

Em resumo, as mudanças no repositório "Sistema-Contratos-Frontend" visam melhorar a experiência do usuário, corrigir problemas existentes e preparar o sistema para crescimento e novas funcionalidades. Essas melhorias refletem o compromisso contínuo em tornar o sistema mais robusto, eficiente e fácil de usar.

---
*Post gerado automaticamente a partir dos commits [`bd0a0f0`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/bd0a0f0deee78cd0bfa9e39e2444306d8000faea), [`df81eba`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/df81eba98ffced2055df64d7359e12d0137bca50), [`7f41109`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/7f4110953bc7140a26abedc5dd26b96fdf61599b), [`b6a0d93`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/b6a0d93476a2834f0416eebec0e6319d74e42ad8), [`98be341`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/98be3418869a6c75c62e34f63b19bc255d28340b), [`058ee04`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/058ee0447872229eda50a2373ee973b18edef7c3), [`621bfda`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/621bfdae981d6793edf753d22280a2f61eb6cef3) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*