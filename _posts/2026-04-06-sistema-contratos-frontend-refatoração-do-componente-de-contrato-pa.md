---
layout: post
title: "Refatoração do componente de contrato para melhorar a exibição de vigência"
date: 2026-04-06 14:15:06 +0000
categories: [Frontend]
tags: ["Sistema Contratos Frontend", "TypeScript", "React", "UI"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

## O que foi feito

Neste commit, realizamos uma refatoração no componente `ContratoCard` localizado no arquivo `src/app/(protected)/contratos/ContratosPageComponents.tsx` do repositório `Sistema-Contratos-Frontend`. A mudança foi feita para melhorar a apresentação da vigência dos contratos, tornando-a mais clara e intuitiva para os usuários.

A alteração específica foi feita na linha 247 do arquivo `ContratosPageComponents.tsx`, onde o texto que exibe a vigência do contrato foi ajustado. Anteriormente, o texto era "Vigencia (Atualizada)", e agora foi simplificado para apenas "Vigencia". Isso faz com que a informação seja apresentada de forma mais direta e sem a necessidade de especificar se a vigência foi atualizada.

```jsx
<p className="flex items-center gap-1.5 text-xs font-semibold text-[#18a7d0] md:text-sm">
  Vigencia: {fmtDate(getInicioVigencia(contrato))} a{" "}
  {fmtDate(getFimVigencia(contrato))}
  <CalendarDays className="h-4 w-4" />
</p>
```

A mudança foi feita por AndreMicael no commit `f212f5d` e resultou na adição de 1 linha e remoção de 1 linha no arquivo afetado.

## Por que foi feito

A motivação por trás desta mudança foi melhorar a experiência do usuário ao visualizar as informações de vigência dos contratos. A palavra "Atualizada" poderia causar confusão ou dar a impressão de que há uma ação necessária por parte do usuário. Ao remover essa palavra, a interface se torna mais clara e fácil de entender.

Além disso, essa mudança pode estar preparando o terreno para futuras melhorias ou novas funcionalidades relacionadas à gestão de contratos, onde uma exibição clara e concisa da vigência seja fundamental.

## Impacto

O resultado prático desta mudança é que os usuários agora terão uma apresentação mais direta e intuitiva da vigência dos contratos. Isso pode levar a uma melhor compreensão das informações apresentadas e, consequentemente, a uma experiência mais eficiente e produtiva ao usar o sistema.

Não se identificam riscos significativos com essa mudança, uma vez que apenas o texto de apresentação foi ajustado, sem afetar a funcionalidade ou lógica por trás da exibição da vigência dos contratos. No entanto, é sempre importante realizar testes cuidadosos após qualquer alteração para garantir que nenhuma funcionalidade tenha sido afetada negativamente.

Com essa refatoração, o sistema `Sistema-Contratos-Frontend` se torna mais amigável e eficaz para os usuários, melhorando a experiência geral ao gerenciar contratos.

---
*Post gerado automaticamente a partir dos commits [`f212f5d`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/f212f5ddda7c0f600d67e13e734d05748a67935a) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*