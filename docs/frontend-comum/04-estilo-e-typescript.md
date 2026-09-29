# Frontend comum — Estilo (Tailwind) e TypeScript

## Estilo (Tailwind CSS v4)

- Tema único em `packages/config/tailwind/theme.css` (tokens de cor, fonte, espaçamento) — os dois apps ficam visualmente consistentes.
- Cada app declara em `globals.css`:

```css
@import 'tailwindcss';
@import '@bot-varejo/config/tailwind/theme.css';
@source '../../../packages/ui/src';   /* garante que classes usadas no UI kit entrem no CSS final */
```

- Classes utilitárias direto no JSX; componentes repetidos viram componentes em `packages/ui`, não `@apply`.

## TypeScript

`packages/config/tsconfig/base.json`:

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

Cada app adiciona `"paths": { "@/*": ["./src/*"] }`.

- Proibido `any` (`@typescript-eslint/no-explicit-any: error`). Use `unknown` + *narrowing*.
- Tipos de API **nunca** são escritos à mão: derivam de `components['schemas'][...]`.
