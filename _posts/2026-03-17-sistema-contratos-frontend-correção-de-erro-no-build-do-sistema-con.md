---
layout: post
title: "Correção de Erro no Build do Sistema-Contratos-Frontend"
date: 2026-03-17 14:12:07 +0000
categories: [Frontend]
tags: ["bugfix", "TypeScript", "Sistema Contratos Frontend", "API"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

## Introdução
No repositório Sistema-Contratos-Frontend, localizado em https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend, foi identificado e corrigido um erro no build do sistema. Este erro estava afetando a funcionalidade de rotas relacionadas a empresas e sua exclusão. Neste artigo, exploraremos o que foi feito e por que essas mudanças foram necessárias.

## O Problema
O problema estava relacionado à forma como os parâmetros de rota eram processados em dois arquivos específicos: `src/app/api/empresas/[id]/route.ts` e `src/app/api/empresas/delete/[id]/route.ts`. Especificamente, o parâmetro `id` não estava sendo tratado corretamente, o que poderia levar a erros ao tentar acessar ou excluir empresas com base no seu ID.

## A Solução
Para resolver esse problema, o commit `f9c9d44` foi realizado pelo desenvolvedor AndreMicael. As principais mudanças foram feitas nos arquivos mencionados anteriormente e envolveram a alteração do tipo de `params` de um objeto com um `id` de tipo `string` para um `Promise` que resolve um objeto com um `id` de tipo `string`. Isso significa que agora os parâmetros de rota precisam ser esperados com `await` antes de serem utilizados.

### Detalhes da Implementação
As mudanças específicas feitas nos arquivos podem ser resumidas da seguinte forma:
- **Alteração do Tipo de `params`**: De `{ params: { id: string } }` para `{ params: Promise<{ id: string }> }`.
- **Uso de `await` para Obter `id`**: `const { id: idParam } = await params;` e posteriormente `const id = Number(idParam);`.
- **Manutenção da Lógica de Validação**: A lógica que verifica se o `id` é um número inteiro positivo foi mantida, apenas adaptada para trabalhar com o novo tratamento assíncrono dos parâmetros.

### Exemplo de Mudança
Antes:
```typescript
export async function GET(
  _req: NextRequest,
  { params }: { params: { id: string } },
) {
  const id = Number(params.id);
  // ...
}
```
Depois:
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

## Conclusão
As mudanças realizadas no repositório Sistema-Contratos-Frontend, especificamente no commit `f9c9d44`, visam corrigir um erro no build relacionado ao processamento de parâmetros de rota. Essas alterações são cruciais para garantir a estabilidade e funcionalidade correta do sistema, especialmente em operações de leitura e exclusão de empresas. Com essas mudanças, o sistema se torna mais robusto e preparado para lidar com requisições de maneira assíncrona, o que é essencial para aplicações modernas de frontend.

---
*Post gerado automaticamente a partir dos commits [`f9c9d44`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/f9c9d440004a8c183035d40d76dc407fb049637a) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*