---
layout: post
title: "Atualização do backend do Sistema de Contratos com melhorias nos controllers e schema do Prisma"
date: 2026-03-12 18:35:04 +0000
categories: [Backend]
tags: ["Sistema Contratos Backend", "JavaScript", "banco de dados", "TypeScript", "documentação", "CI/CD"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Backend"
---

## O que foi feito

Nesta atualização, fizemos várias mudanças importantes no backend do Sistema de Contratos para melhorar a performance, corrigir bugs e adicionar novas funcionalidades. Abaixo, vamos descrever cada uma dessas mudanças de forma detalhada.

### Correções nos erros de endereço no backend

No commit `3936c49`, corrigimos erros de endereço no backend, alterando o arquivo `prisma/schema.prisma` e `src/controllers/pessoas.controller.ts`. No arquivo `prisma/schema.prisma`, mudamos a relação entre `pessoa_endereco` e `pessoas_instituicoes` para corrigir um problema de consistência de dados. Adicionalmente, criamos novos modelos de dados para `porte_empresa`, `fornecedor_pessoa_fisica` e `fornecedor_pessoa_juridica` para atender a novas necessidades do sistema.

```prisma
model pessoa_endereco {
  id_endereco          Int                  @id @default(autoincrement())
  id_fornecedor        Int
  cep                  String?              @db.VarChar(20)
  logradouro           String?              @db.VarChar(255)
  numero               String?              @db.VarChar(20)
  // ...
}

model porte_empresa {
  id_porte_empresa     Int                    @id @default(autoincrement())
  codigo               String                 @unique(map: "uk_porte_empresa_codigo") @db.VarChar(10)
  descricao            String                 @db.VarChar(100)
  ativo                Boolean                @default(true)
  data_criacao         DateTime               @default(now()) @db.Timestamp(6)
  data_atualizacao     DateTime?              @db.Timestamp(6)
  Usuario              Usuario[]
  pessoas_instituicoes pessoas_instituicoes[]
}
```

### Adaptações nos controllers para aceitar nome fantasia para MEI

No commit `f034105`, fizemos adaptações no `pessoas.controller.ts` para permitir que o sistema aceite nome fantasia para Microempreendedores Individuais (MEI). Isso foi feito para atender a uma nova exigência legal que permite que MEI tenham um nome fantasia além do nome civil.

```typescript
if (tipo_pessoa === 'PJ') {
  dataPessoa.data_fundacao = dataFundDate;
  // Permite porte também para PF; quando não informado, fica null
  dataPessoa.id_porte_empresa = id_porte_empresa ?? null;
}
```

### Correção da rota pessoas

No commit `142abf5`, corrigimos a rota `pessoas` no arquivo `src/controllers/pessoas.controller.ts`. Isso envolveu a criação de funções auxiliares para lidar com as consultas ao banco de dados de forma mais eficiente e legível.

```typescript
function pessoas(prisma: any) {
  return prisma.pessoas_instituicoes;
}

function enderecos(prisma: any) {
  return prisma.pessoa_endereco;
}
```

### Correção de departamentos backend

No commit `45963c2`, corrigimos o controller de departamentos, removendo código desnecessário e melhorando a legibilidade.

### Integração de branches e configuração de deploy

No commit `803156a`, realizamos a integração de branches e configuramos o deploy para exigir aprovação de duas pessoas diferentes antes de enviar as alterações para produção. Isso foi feito editando o arquivo `.github/workflows/node.js.yml` e adicionando um arquivo `.github/DEPLOY-APPROVAL.md` com as instruções para a configuração do deploy protegido.

## Por que foi feito

As mudanças foram feitas para corrigir problemas existentes, melhorar a performance e atender a novas exigências legais e de negócios. A correção dos erros de endereço foi necessária para garantir a consistência dos dados armazenados no banco de dados. A adaptação para aceitar nome fantasia para MEI foi uma exigência legal recente. A correção da rota pessoas e a melhoria no controller de departamentos visaram melhorar a eficiência e a legibilidade do código.

A integração de branches e a configuração do deploy com aprovação de duas pessoas diferentes foram feitas para garantir a qualidade e a segurança das alterações enviadas para produção. Isso ajuda a prevenir erros críticos e garantir que as atualizações sejam testadas e

---
*Post gerado automaticamente a partir dos commits [`3936c49`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/3936c496b2107e435a960c33a100b5367716490d), [`f034105`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/f03410587ec2c268dbcb8a6346635db64c90da44), [`142abf5`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/142abf5376ca8c506bdbd45d763ee010c9383525), [`45963c2`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/45963c28b4f77ee0588af597eaf273ee579c6434), [`803156a`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/803156ad8b8ccf0f91b0469a9c86eb7f34603b6e) em [Sistema-Contratos-Backend](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend)*