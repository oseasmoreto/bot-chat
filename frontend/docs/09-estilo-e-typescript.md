# 09 — Estilo (Tailwind) e TypeScript

## Estilo (Tailwind CSS v4)

- Tema único em `src/app/globals.css` via `@theme` (tokens de cor, fonte, espaçamento) — web e admin compartilham os tokens; cada área pode ter variações no seu *shell*.
- `src/app/globals.css`:

```css
@import 'tailwindcss';

@theme {
  --color-brand-500: oklch(0.62 0.19 255);
  --color-status-ok: oklch(0.72 0.17 150);
  --color-status-degraded: oklch(0.80 0.16 85);
  --color-status-down: oklch(0.63 0.22 25);
  --font-sans: 'Inter', system-ui, sans-serif;
}
```

- Classes utilitárias direto no JSX; componentes repetidos viram componentes em `src/shared/ui`, não `@apply`.
- Cores de status (`ok`, `degraded`, `down`) sempre pelos tokens — nunca hex solto.

## TypeScript

`tsconfig.json`:

```json
{
  "compilerOptions": {
    "target": "ES2022",
    "lib": ["dom", "dom.iterable", "ES2022"],
    "module": "esnext",
    "moduleResolution": "bundler",
    "jsx": "preserve",
    "strict": true,
    "noUncheckedIndexedAccess": true,
    "noImplicitOverride": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true,
    "isolatedModules": true,
    "resolveJsonModule": true,
    "skipLibCheck": true,
    "noEmit": true
  }
}
```

Mais o necessário para o Next: `"plugins": [{ "name": "next" }]`, `"paths": { "@/*": ["./src/*"] }` e `"include": ["next-env.d.ts", "src", "e2e", ".next/types/**/*.ts"]`.

- Proibido `any` (`@typescript-eslint/no-explicit-any: error`). Use `unknown` + *narrowing*.
- Tipos de API **nunca** são escritos à mão: derivam de `components['schemas'][...]` em `@/shared/api/schema`.
