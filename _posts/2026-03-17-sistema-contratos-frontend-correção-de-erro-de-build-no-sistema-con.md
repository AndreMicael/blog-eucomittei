---
layout: post
title: "Correção de Erro de Build no Sistema-Contratos-Frontend"
date: 2026-03-17 14:12:07 +0000
categories: [Frontend]
tags: ["Sistema Contratos Frontend", "API", "TypeScript", "bugfix"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

O repositório Sistema-Contratos-Frontend, hospedado no GitHub, sofreu uma importante atualização recentemente. O commit `f9c9d44`, realizado por AndreMicael em 17 de março de 2026, visou corrigir um erro de build que estava afetando o sistema.

## O Problema
O erro de build era causado por uma incompatibilidade nos tipos de dados dos parâmetros de rota. Especificamente, o arquivo `src/app/api/empresas/[id]/route.ts` esperava que o parâmetro `id` fosse uma string, enquanto o arquivo `src/app/api/empresas/delete/[id]/route.ts` esperava que o parâmetro `id` fosse um número.

## A Solução
Para corrigir o erro, o autor do commit atualizou os arquivos `src/app/api/empresas/[id]/route.ts` e `src/app/api/empresas/delete/[id]/route.ts` para usar um tipo de dado mais flexível para o parâmetro `id`. Ele mudou o tipo de `params` de `{ params: { id: string } }` para `{ params: Promise<{ id: string }> }`, o que permite que o parâmetro `id` seja lido de forma assíncrona.

Além disso, ele adicionou uma linha de código para extrair o valor de `id` do objeto `params` usando a desestruturação de objeto: `const { id: idParam } = await params;`. Em seguida, ele converte o valor de `idParam` para um número usando a função `Number()`.

## Código Atualizado
O código atualizado para a rota `GET` agora se parece com isso:
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
E o código atualizado para a rota `PATCH` agora se parece com isso:
```typescript
export async function PATCH(
  req: NextRequest,
  { params }: { params: Promise<{ id: string }> },
) {
  const { id: idParam } = await params;
  const id = Number(idParam);
  if (!Number.isInteger(id) || id <= 0) {
    return jsonResponse({ error: "ID inválido" }, 400);
  }
  // ...
}
```
## Conclusão
A correção do erro de build no Sistema-Contratos-Frontend demonstra a importância de manter o código atualizado e compatível com as últimas versões das dependências e frameworks utilizadas. Com essa atualização, o sistema deve funcionar corretamente e sem erros de build. Além disso, a alteração nos tipos de dados dos parâmetros de rota melhora a flexibilidade e a robustez do código, permitindo que o sistema seja mais escalável e fácil de manter.

---
*Post gerado automaticamente a partir dos commits [`f9c9d44`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/f9c9d440004a8c183035d40d76dc407fb049637a) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*