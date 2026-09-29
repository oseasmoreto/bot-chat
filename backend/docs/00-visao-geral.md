# 00 — Visão geral (backend)

## Contexto

O **Bot Varejo** é a plataforma de atendimento, via chat, de serviços oferecidos por parceiros de varejo. O sistema tem dois projetos independentes, cada um com repositório, documentação e deploy próprios:

| Projeto | Domínio | Responsabilidade |
|---------|---------|------------------|
| **Backend** (este) | `api.<dominio>` | APIs REST e WebSocket para os escopos `public` e `admin`; base para fluxos e integrações |
| Frontend | `app.<dominio>` | App Next.js com as áreas web (`/`) e admin (`/admin`) |

O backend atende dois **escopos**:

| Escopo | Consumidor | Exemplo de uso futuro |
|--------|------------|------------------------|
| `public` | Área web do frontend (cliente final) | Conversar com o bot, contratar/consultar serviços |
| `admin` | Área admin do frontend (operadores, parceiros) | Construir fluxos, configurar integrações, acompanhar atendimentos |

## Stack

| Item | Tecnologia |
|------|------------|
| Linguagem | Python 3.13 |
| Framework | FastAPI (async) + Uvicorn |
| Tempo real | WebSockets (Starlette/FastAPI) |
| Validação / schemas | Pydantic v2, pydantic-settings |
| Banco de dados | Amazon DynamoDB — uma tabela por bounded context, acesso async com aioboto3; DynamoDB Local em dev/testes |
| Dependências | uv |
| Qualidade | ruff, mypy `--strict`, import-linter |
| Testes | pytest, pytest-asyncio, httpx |
| Container | Imagem `python:3.13-slim`, Uvicorn direto |
| Documentação da API | OpenAPI 3.1 + Swagger UI (`/api/docs`) + ReDoc (`/api/redoc`) |

## Princípios

| Princípio | Como se aplica no backend |
|-----------|---------------------------|
| **DDD** | Bounded contexts; domínio sem dependência de framework |
| **SOLID** | Casos de uso com responsabilidade única; dependências por `Protocol` |
| **DRY** | Router factory por escopo; `BaseSchema` central; handlers WS reutilizam casos de uso |
| **KISS** | Sem DI framework, sem ORM, sem broker enquanto não forem necessários |
| **TDD** | Teste antes do código; nenhuma rota/mensagem sem teste |
| **Tipagem forte** | `mypy --strict`, Pydantic, contrato OpenAPI gerado |

## Tarefas

Objetivo, critérios de aceitação e escopo de cada tarefa ficam em [tasks/](./tasks/README.md).
