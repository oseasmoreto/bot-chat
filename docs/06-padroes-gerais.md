# 06 — Padrões gerais de código

## 1. Nomenclatura

A orientação da task é **camelCase para métodos**. Aplicamos assim ([ADR-0008](./adr/0008-convencao-de-nomes.md)):

- **TypeScript:** camelCase em funções, métodos e variáveis — padrão da linguagem.
- **Python:** seguimos a **PEP 8** (`snake_case` em funções/métodos), que é o padrão da linguagem e é exigido pelo `ruff` (regra `N802`). Usar camelCase no Python iria contra todo o ecossistema (FastAPI, Pydantic, stdlib).
- **Fronteira (JSON da API, mensagens WS, operationId):** **camelCase**. O Python converte automaticamente via `BaseSchema`, então quem consome a API só vê camelCase.

Detalhes por linguagem:

| Linguagem | Documento |
|-----------|-----------|
| Python (backend) | [backend/08-padroes-python.md](./backend/08-padroes-python.md) |
| TypeScript/React (web e admin) | [frontend-comum/05-padroes-typescript.md](./frontend-comum/05-padroes-typescript.md) |

### 1.1 API e mensagens

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Campo JSON | camelCase | `uptimeSeconds` |
| Path | kebab-case, plural | `/api/v1/admin/partner-services` |
| operationId | camelCase | `getAdminHealth` |
| Tipo de mensagem WS | `contexto.acao` minúsculo | `health.ping` |
| Código de erro | snake_case | `unknown_message_type` |

## 2. Boas práticas gerais
- **Funções pequenas** com uma responsabilidade; se precisa de "e" para descrever, divida.
- **Early return** em vez de `if` aninhado.
- **Sem números/strings mágicos**: constantes nomeadas.
- **Imutabilidade por padrão** (`frozen=True`, `readonly`, `as const`).
- **Comentários explicam o porquê**, não o quê. Código auto-explicativo dispensa comentário.
- **Sem código morto** nem comentado — o git guarda o histórico.
- **Sem segredos no código** — variáveis de ambiente; `.env` nunca é commitado.
- Textos da interface em **pt-BR**; código (nomes) em **inglês**.

## 3. Formatação e lint

| Ferramenta | Escopo | Config |
|------------|--------|--------|
| `ruff format` | Python | `line-length = 100` |
| `ruff check` | Python | regras em [backend — pyproject.toml](./backend/08-padroes-python.md#configuração-das-ferramentas-pyprojecttoml) |
| `mypy` | Python | `strict = true` |
| `import-linter` | Python | fronteiras de camadas DDD |
| Prettier | TS/TSX/CSS/JSON/MD | `singleQuote: true`, `semi: true`, `trailingComma: 'all'`, `printWidth: 100` |
| ESLint | TS/TSX | `@bot-varejo/config/eslint` (typescript-eslint strict, react-hooks, jsx-a11y, boundaries, import order) |
| EditorConfig | todos | UTF-8, LF, indent 2 (TS) / 4 (Python), newline final |
| pre-commit | todos | roda ruff, mypy, prettier e eslint nos arquivos alterados |
