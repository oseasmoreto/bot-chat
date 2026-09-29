# ADR-0003 — Roteamento por prefixo de path

- **Status:** Aceito
- **Data:** 2026-09-29
- **Ticket:** CPBS-275

## Contexto
Precisamos separar os escopos `public` e `admin` tanto nos frontends quanto na API.

## Decisão
Mesmo domínio, separação por path:

| Path | Destino |
|------|---------|
| `/` | web (public) |
| `/admin` | admin |
| `/api/v1/public/*`, `/api/v1/admin/*` | FastAPI REST |
| `/ws/public`, `/ws/admin` | FastAPI WebSocket |
| `/api/docs`, `/api/openapi.json` | Swagger / OpenAPI |

## Alternativas consideradas
- **Subdomínios** (`admin.dominio`): exige DNS/hosts locais e certificados extras; pode ser adotado depois, pois o Nginx isola essa decisão.

## Consequências
- Tudo na mesma origem → **sem CORS**, URLs relativas no front.
- App admin usa `basePath: '/admin'` no Next.
- O app `web` não pode ter rota `/admin`.
- Quando houver autenticação, cookies do admin devem usar `Path=/admin`/`/api/v1/admin` conforme o desenho de auth (futuro).
