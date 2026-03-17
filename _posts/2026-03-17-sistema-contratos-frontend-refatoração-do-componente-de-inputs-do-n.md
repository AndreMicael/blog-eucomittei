---
layout: post
title: "Refatoração do Componente de Inputs do Novo Contrato e Correção de Bugs no Frontend do Sistema de Contratos"
date: 2026-03-17 14:12:07 +0000
categories: [Frontend]
tags: ["feature", "React", "TypeScript", "UI", "Sistema Contratos Frontend", "bugfix"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

## O que foi feito

Nesta série de commits, várias mudanças foram realizadas no repositório "Sistema-Contratos-Frontend" para melhorar a estabilidade e a usabilidade do sistema. As principais alterações incluem:

- **Commit 1 (`f9c9d44`)**: Corrigiu um erro no build, alterando a forma como os parâmetros são tratados nas rotas de empresa. Isso foi feito em `src/app/api/empresas/[id]/route.ts` e `src/app/api/empresas/delete/[id]/route.ts`, mudando o tipo de `params` para `Promise<{ id: string }>`, garantindo que o `id` seja processado corretamente antes de ser utilizado.

  ```typescript
  export async function GET(
    _req: NextRequest,
    { params }: { params: Promise<{ id: string }> },
  ) {
    const { id: idParam } = await params;
    const id = Number(idParam);
    // ...
  }
  ```

- **Commit 2 (`4ff3df4`)**: Melhorou os inputs do Novo Contrato, alterando a classe CSS em `src/app/(protected)/contratos/novo/NovoContratoComponents.tsx`. A mudança foi na classe do `div` que envolve os inputs, melhorando a aparência.

  ```tsx
  <div className="flex min-w-[72px]  flex-col items-center gap-2">
    {/* ... */}
  </div>
  ```

- **Commit 3 (`54885ac`)**: Corrigiu os inputs de descrição em várias etapas do novo contrato, mudando classes CSS para melhorar a aparência e a consistência. Isso afetou `src/app/(protected)/contratos/novo/Etapas/DadosContrato.tsx`, `Gestao.tsx`, `Partes.tsx` e `SaldosEVigencias.tsx`.

  ```tsx
  const fieldCls =
    "flex min-w-0 items-center gap-2 rounded-lg bg-zinc-50 border border-zinc-300 bg-white px-3 py-2.5 transition focus-within:border-blue-primary focus-within:ring-1 focus-within:ring-blue-primary/30";
  ```

- **Commit 4 (`554488b`)**: Melhorou o design dos inputs do Novo Contrato, focando na etapa de Gestão. Alterações incluíram a remoção de um header azul e a reorganização de alguns componentes em `src/app/(protected)/contratos/novo/Etapas/Gestao.tsx`, `Partes.tsx` e `SaldosEVigencias.tsx`.

  ```tsx
  {/* <div className="shrink-0 bg-blue-primary px-6 py-5"> */}
  {/* ... */}
  {/* </div> */}
  ```

- **Commit 5 (`5191af7`)**: Adicionou um datepicker personalizado nos inputs de data, melhorando a usabilidade. Isso foi feito em `src/app/(protected)/contratos/novo/Etapas/Gestao.tsx`, com a importação de `DatePickerCally` e sua integração nos campos de data.

  ```tsx
  import { DatePickerCally } from "@/components/DatePickerCally";
  // ...
  <DatePickerCally
    value={form.dataInicioGestao}
    onChange={(value) => setDate("dataInicioGestao")(value)}
  />
  ```

## Por que foi feito

Essas mudanças foram realizadas para melhorar a experiência do usuário no sistema de contratos, tanto em termos de usabilidade quanto de estabilidade. A correção de bugs, como o erro no build, foi essencial para garantir que o sistema funcionasse corretamente. As melhorias nos inputs do Novo Contrato e na etapa de Gestão visam facilitar o preenchimento de informações pelos usuários, tornando-o mais intuitivo e agradável.

A adição do datepicker personalizado nos inputs de data foi uma melhoria significativa, pois permite aos usuários selecionar datas de forma mais intuitiva e precisa, reduzindo erros de digitação.

## Impacto

O impacto dessas mudanças é positivo, melhorando a estabilidade do sistema e a experiência do usuário. Com as correções de bugs, o sistema deve ser menos propenso a erros e mais confiável. As melhorias na interface do usuário, especialmente a inclusão do datepicker, tornam o

---
*Post gerado automaticamente a partir dos commits [`f9c9d44`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/f9c9d440004a8c183035d40d76dc407fb049637a), [`4ff3df4`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/4ff3df480a5d15dc94dba44031254d200c1fb2f2), [`54885ac`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/54885ac5cc4d527b2166a6b1adc389919bd17fe3), [`554488b`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/554488bc88bc014b4984bcd49cb9aa7cc493dfd1), [`5191af7`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/5191af7f2eaf83242928b991f1a29420f1be925e) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*