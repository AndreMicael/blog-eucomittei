---
layout: post
title: "Correção de Erro de Logout e Melhorias na Interface de Usuário"
date: 2026-04-01 13:00:24 +0000
categories: [Frontend]
tags: ["React", "autenticação", "API", "TypeScript", "Sistema Contratos Frontend", "UI"]
repo: "https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend"
---

O repositório `Sistema-Contratos-Frontend` sofreu recentemente uma série de mudanças importantes, visando melhorar a experiência do usuário e corrigir problemas críticos, especialmente relacionados ao processo de logout. Neste post, vamos explorar detalhadamente o que foi feito, por que foi feito e como essas mudanças afetam o sistema.

## O que foi feito

### Commit 84955ff: Trocando a URL de Logout no Botão de Sair

Neste commit, houve uma modificação no arquivo `components/Sidebar.tsx`. A mudança visava corrigir a URL de redirecionamento após o logout, garantindo que o usuário seja redirecionado corretamente para a página de login após sair do sistema. O trecho de código alterado pode ser visto abaixo:

```typescript
const handleLogout = () => {
  setShowUserMenu(false);
  if (typeof window !== "undefined") {
    const rawBasePath = process.env.NEXT_PUBLIC_BASE_PATH ?? "/contratos-frontend";
    const basePath = rawBasePath.replace(/\/$/, "");
    window.location.href = `${basePath}/api/auth/logout`;
  }
};
```

### Commit 668e320: Corrigindo Erro do Logout

Este commit corrigiu um problema no arquivo `src/app/api/auth/logout/route.ts`, relacionado à lógica de redirecionamento após o logout. A função `getLoginRedirectUrl` foi reestruturada para `normalizeBasePath` para simplificar a obtenção da URL de redirecionamento, considerando a base do path de forma mais robusta. O código relevante é o seguinte:

```typescript
function normalizeBasePath(basePath: string): string {
  const trimmed = basePath.trim().replace(/\/$/, "");
  if (!trimmed) return "";
  return trimmed.startsWith("/") ? trimmed : `/${trimmed}`;
}

export async function GET(request: NextRequest) {
  const basePath = normalizeBasePath(process.env.NEXT_PUBLIC_BASE_PATH ?? "");
  const loginUrl = new URL(`${basePath}/login`, request.nextUrl.origin);
  const response = NextResponse.redirect(loginUrl);
  clearSessionCookieOnResponse(response);
  return response;
}
```

### Commit 4e53914: Merge de Branch e Mudanças na Interface

Embora este commit seja um merge da branch `dev` para a branch `production`, ele também trouxe uma serie de mudanças na interface de usuário, incluindo a adição de uma nova cor para labels (`labelText: "#64748b"`) e melhorias no componente `ActionButton`, como a adição da propriedade `disabled` para controlar a aparência e funcionalidade do botão quando estiver desabilitado.

```typescript
export function ActionButton({
  // ...
  disabled,
}: {
  // ...
  disabled?: boolean;
}) {
  const cls = "inline-flex items-center gap-1.5 rounded-md border px-3 py-1.5 text-xs font-semibold transition cursor-pointer";
  // ...
  return (
    <button
      type="button"
      onClick={onClick}
      disabled={disabled}
      className={cls}
      style={{
        ...style,
        opacity: disabled ? 0.55 : 1,
        cursor: disabled ? "not-allowed" : "pointer",
      }}
    >
      {children}
    </button>
  );
}
```

## Por que foi feito

As mudanças foram motivadas pela necessidade de corrigir problemas críticos de logout que afetavam a experiência do usuário e a segurança do sistema. Além disso, melhorias na interface de usuário visam proporcionar uma experiência mais agradável e intuitiva para os usuários do sistema.

## Impacto

Essas mudanças têm um impacto positivo direto na experiência do usuário. A correção do processo de logout garante que os usuários sejam redirecionados corretamente para a página de login após sair do sistema, o que era um problema que causava confusão. As melhorias na interface de usuário, como a adicionação da propriedade `disabled` no componente `ActionButton` e as mudanças nas cores, contribuem para uma interface mais consistente e fácil de usar.

Em resumo, as mudanças feitas no repositório `Sistema-Contratos-Frontend` são cruciais para a melhoria contínua do sistema, tanto em termos de funcionalidade quanto de experiência do usuário. Essas melhorias reforçam o compromisso de entregar um sistema seguro, estável e agradável de usar.

---
*Post gerado automaticamente a partir dos commits [`84955ff`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/84955ff160b0456d05a21436a1953a5ed4d03964), [`668e320`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/668e320f053d26df39cef815eeb64f4e2309b75f), [`4e53914`](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend/commit/4e53914d4d33949dc4e7bf14ae32fbd85d71845f) em [Sistema-Contratos-Frontend](https://github.com/Desenvolve-MT/Sistema-Contratos-Frontend)*