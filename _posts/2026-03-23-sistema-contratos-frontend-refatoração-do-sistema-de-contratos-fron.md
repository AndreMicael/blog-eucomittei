---
layout: post
title: "Refatoração do Sistema de Contratos Frontend para Melhor Gerenciamento de Erros e Interfaces"
date: 2026-03-23 19:16:03 +0000
categories: [Frontend]
tags: ["React", "UI", "TypeScript", "bugfix", "feature", "Sistema Contratos Frontend"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

## O que foi feito

Nas últimas atualizações do repositório "Sistema-Contratos-Frontend", várias mudanças importantes foram implementadas para melhorar a gestão de erros, a responsividade da interface e a usabilidade geral do sistema. Os commits realizados abordam desde a melhoria no tratamento de erros de API até ajustes nos componentes de interface para uma experiência mais fluída e intuitiva.

Um dos principais pontos de mudança foi a melhoria no tratamento de erros de API, como evidenciado no commit `22aeab3`. Nele, foi adicionada uma funcionalidade para lidar melhor com erros de API, notadamente no componente `NovoUsuarioForm.tsx` e em outros arquivos como `DepartamentosComponents.tsx`. Por exemplo, no `NovoUsuarioForm.tsx`, foi implementado um catch para exibir mensagem de erro quando não for possível carregar unidades e departamentos:

```tsx
catch {
  setError(
    "Não foi possível carregar unidades e departamentos. Verifique a conexão com o servidor.",
  );
}
```

Além disso, houve ajustes nas classes de Tailwind para melhorar a aparência e a responsividade dos componentes, como visto no commit `175a1cc`. Isso incluiu mudanças em componentes como o `Navbar.tsx` e o `Toast.tsx`, visando uma melhor apresentação em diferentes dispositivos e tamanhos de tela.

Outra área de melhoria foi a correção de rotas conflitantes, como mostrado no commit `956b588`. Isso ajudou a resolver problemas de navegação dentro do sistema, garantindo que os usuários possam se mover entre diferentes seções sem encontrar erros de rota.

A adição de toasts (notificações flutuantes) nos fluxos que ainda não as possuíam, conforme o commit `7dc4057`, melhorou a experiência do usuário, fornecendo feedback imediato sobre ações realizadas, como a criação de novos usuários ou instituições.

Por fim, um commit específico (`17c6a9a`) foi dedicado a corrigir um erro na imagem de avatar no componente de navbar, garantindo que as imagens sejam exibidas corretamente e melhorando a aparência geral da barra de navegação.

## Por que foi feito

Essas mudanças foram motivadas pela necessidade de melhorar a usabilidade e a confiabilidade do sistema. O tratamento de erros foi aprimorado para fornecer aos usuários mensagens claras e úteis quando algo der errado, ajudando a reduzir a frustração e aumentar a eficiência. As melhorias na interface visam facilitar a navegação e a interação, tornando o sistema mais acessível e agradável de usar.

Além disso, a correção de erros e a melhoria na gestão de rotas contribuem para a estabilidade do sistema, minimizando a chance de erros inesperados e melhorando a experiência geral do usuário.

## Impacto

O impacto prático dessas mudanças é significativo. Os usuários agora têm uma experiência mais fluida e intuitiva, com menos interrupções devido a erros. A melhoria no tratamento de erros de API ajuda a identificar e resolver problemas de forma mais eficiente, reduzindo o tempo gasto em depuração.

As melhorias na interface e a adição de toasts para notificações proporcionam uma experiência mais moderna e responsiva, alinhada com as expectativas dos usuários em relação a aplicativos web atuais. A correção de erros específicos, como o problema com a imagem de avatar no navbar, demonstra atenção ao detalhe e um compromisso com a qualidade.

No entanto, é importante notar que, como em qualquer atualização de software, há um risco de introduzir novos bugs ou problemas inesperados. Portanto, é crucial continuar monitorando o desempenho do sistema e coletar feedback dos usuários para identificar e corrigir qualquer problema que possa surgir.

---
*Post gerado automaticamente a partir dos commits [`22aeab3`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/22aeab3d0b2eb998015f599513ce53c237dd3e37), [`175a1cc`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/175a1cc4c793a6ed9013e54009fe55d86402d9bb), [`956b588`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/956b588cef500f5ba7f5f850c49932a376f96e12), [`7dc4057`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/7dc4057be89dec1d2d3d54b3fa1a52717208b9d9), [`17c6a9a`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/17c6a9acb71d59a49b4b6bc4628a055ce7797eb9) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*