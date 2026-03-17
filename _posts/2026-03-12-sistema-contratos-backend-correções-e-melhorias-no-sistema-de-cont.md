---
layout: post
title: "Correções e Melhorias no Sistema de Contratos Backend"
date: 2026-03-12 18:35:04 +0000
categories: [Backend]
tags: ["Sistema Contratos Backend", "banco de dados", "API", "bugfix", "TypeScript"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Backend"
---

O desenvolvimento do Sistema de Contratos Backend continua a avançar com melhorias e correções importantes para garantir a estabilidade e a funcionalidade do sistema. Neste post, vamos explorar as mudanças introduzidas pelo commit `3936c49`, que visam corrigir erros de endereço no backend e introduzir novas funcionalidades para a gestão de fornecedores e pessoas.

## Correções de Erros de Endereço

O commit em questão corrigiu erros relacionados ao endereço no backend, melhorando a integridade dos dados e evitar problemas futuros. Os arquivos afetados incluem `prisma/schema.prisma` e `src/controllers/pessoas.controller.ts`. Essas alterações são críticas para garantir que o sistema possa lidar corretamente com informações de endereço, o que é fundamental para a gestão eficaz de contratos e relacionamentos com fornecedores e outros stakeholders.

## Novas Funcionalidades para Fornecedores e Pessoas

Além das correções, o commit também introduziu novos modelos de dados para melhorar a gestão de fornecedores e pessoas. Isso inclui a criação de modelos para `fornecedor_pessoa_fisica`, `fornecedor_pessoa_juridica`, `fornecedores`, `socios` e `porte_empresa`. Esses novos modelos permitem uma representação mais detalhada e flexível dos dados relacionados a fornecedores e pessoas, facilitando a gestão de informações complexas e a aplicação de regras de negócio específicas.

### Detalhes das Alterações

As alterações incluem:
- A correção do relacionamento entre `pessoa_endereco` e `pessoas_instituicoes`, trocando `id_pessoa` por `id_fornecedor` para refletir melhor a estrutura de dados.
- A introdução de novos campos em `pessoas_instituicoes` para acomodar as novas funcionalidades, como `porte_empresa`.
- Modificações no controlador `PessoasController` para lidar com as novas regras de negócio e validações de dados.

## Conclusão

As mudanças introduzidas pelo commit `3936c49` são um passo importante na melhoria contínua do Sistema de Contratos Backend. Corrigindo erros de endereço e introduzindo novas funcionalidades para a gestão de fornecedores e pessoas, essas alterações contribuem para uma plataforma mais robusta, escalável e capaz de atender às necessidades complexas de gestão de contratos. A equipe de desenvolvimento continua a trabalhar arduamente para garantir que o sistema atenda aos padrões mais altos de qualidade e funcionalidade.

---
*Post gerado automaticamente a partir dos commits [`3936c49`](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend/commit/3936c496b2107e435a960c33a100b5367716490d) em [Sistema-Contratos-Backend](https://github.com/Desenvolve-MT/Sistema-Contratos-Backend)*