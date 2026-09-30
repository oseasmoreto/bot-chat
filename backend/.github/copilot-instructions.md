# Bot Varejo — Backend: instruções para o GitHub Copilot

API REST + WebSocket do Bot Varejo em **Python 3.13 + FastAPI (async)**, arquitetura **DDD com bounded contexts**, banco **Amazon DynamoDB**. Responda e escreva textos (docs, mensagens de erro, commits) em **pt-BR**; nomes no código em **inglês**.

A documentação em [`docs/`](../docs/README.md) é a fonte da verdade. Na dúvida, siga o código de referência do context `health` (`api/contexts/health/`) e os docs [02 — Estrutura](../docs/02-estrutura.md), [03 — DDD](../docs/03-arquitetura-ddd.md), [04 — Context health](../docs/04-context-health.md) e [10 — Padrões](../docs/10-padroes-codigo.md).

## Antes de construir: análise obrigatória

Toda tarefa que **cria ou altera** comportamento (context, módulo, endpoint, mensagem WebSocket, integração) começa pela **fase de Análise** do agente [backend-ddd](agents/backend-ddd.agent.md): ler o código e os docs, responder sozinho o que já está definido, fazer as perguntas do roteiro (comum + específico da tarefa) de uma vez, cada uma com uma sugestão, e fechar com o resumo de decisões confirmado. Nenhum código antes disso. Tarefas pequenas sem decisão de contrato ou modelo (ex.: corrigir um typo, renomear variável local) dispensam a análise.

## Estrutura

```text
api/
├── app_run.py        # create_app(): middlewares, routers, handlers de erro
├── config.py         # Settings (pydantic-settings, variáveis APP_*)
├── container.py      # composition root: instancia adapters e casos de uso
├── core/             # shared kernel: cors, swagger, logs, errors, request_id, scope, schemas, websocket/
├── routes/           # public.py, admin.py, websocket.py — só composição por escopo
├── contexts/<ctx>/   # domain/ application/ infrastructure/ presentation/
└── scripts/          # python -m api.scripts.<nome>
tests/                # unit/ integration/ contract/ + fakes.py + conftest.py
config/               # deploy/infra da plataforma — NÃO alterar
certificates/         # certificados de CA (.crt) — nunca chaves privadas
```

Imports sempre absolutos a partir de `api` (`from api.core.scope import Scope`). O código não é instalado: rode tudo na raiz do projeto.

## Regras de arquitetura (verificadas pelo import-linter)

| Camada | Pode importar | Nunca importa |
|--------|---------------|---------------|
| `domain` | stdlib, `api.core.scope`, o próprio domínio | FastAPI, Pydantic, Starlette, boto/aioboto3, httpx, tenacity, `application`, `infrastructure`, `presentation` |
| `application` | `domain`, `core` | FastAPI, Starlette, boto/aioboto3, httpx, `infrastructure`, `presentation` |
| `infrastructure` | `domain`, `core`, libs externas | `presentation` |
| `presentation` | `application`, `domain`, `core`, FastAPI, Pydantic | `infrastructure` (recebe tudo via `container.py` + `Depends`) |

- Um context **nunca** importa código interno de outro context nem acessa a tabela dele.
- Dependências entram pelo construtor (casos de uso) e por `Depends` (presentation). Sem framework de DI: o `Container` (dataclass) em `container.py` monta tudo.
- `core/` é mínimo e transversal; nada específico de um context vai para lá.

## Convenções

- **PEP 8** no Python (`snake_case`); **camelCase** no JSON, via `BaseSchema` (`api/core/schemas.py`) — nunca escreva alias à mão.
- Nomes: caso de uso `<Verbo><Substantivo>UseCase` com método `execute`; port `<Nome>Port` ou `<Entidade>Repository` (`typing.Protocol`); adapter com o nome da tecnologia (`DynamoDbPartnerRepository`, `HttpAcmeClient`); schemas `<Nome>Request` / `<Nome>Response`.
- Rotas: prefixo `/api/v1/{public|admin}`, recursos no plural em kebab-case (`/partner-services`), `operation_id` em camelCase (`listAdminPartners`), `summary` e respostas não-2xx em `responses=`.
- Mensagens WebSocket: `type` no formato `contexto.acao` (`partners.list`), envelope `WsMessage` (`type`, `id`, `payload`).
- Erros de negócio: subclasses de `DomainError` (`api/core/errors.py`) com `code` snake_case estável e `status_code`. Nunca retorne stack trace nem `HTTPException` com texto solto.
- Logs: `logger = logging.getLogger(__name__)`, mensagem como evento `contexto.acao` e dados em `extra=`; nunca logue segredos ou dados pessoais.
- Tipagem: `mypy --strict`; toda função anotada; `@dataclass(frozen=True, slots=True, kw_only=True)` no domínio; `Any` só na fronteira, comentado; `# type: ignore[código]  # motivo`.
- `async def` em rotas, casos de uso e adapters de I/O; nada bloqueante no event loop.
- Comentários explicam o **porquê**; sem código morto ou comentado; sem `print`.
- Configuração nova = campo no `Settings` (`api/config.py`) + `.env.example` + tabela de variáveis em `docs/08-docker.md`. Nunca leia `os.environ` direto.

## Testes (TDD, obrigatório)

- Escreva o teste **antes** do código. Toda rota HTTP, mensagem WebSocket e caso de uso tem teste; cobertura mínima 90%.
- Unitários com *fakes* das ports (em `tests/fakes.py`), sem `mock.patch` no domínio. Integração de rota com `client` (httpx `AsyncClient`) e WebSocket com `ws_client` (`TestClient`) de `tests/conftest.py`.
- Nome: `test_<comportamento>_when_<condição>`; Arrange / Act / Assert separados por linha em branco.

## Dependências

`requirements.txt` (runtime) e `requirements-test.txt` (testes e qualidade), sempre com `==`. Lib nova: linha no arquivo certo + tabela em [docs/13 — Dependências](../docs/13-dependencias.md). Nunca use outro gerenciador de pacotes nem coloque dependências no `pyproject.toml`.

## Validação antes de concluir

Na raiz do projeto. Com `make` (Linux, macOS, WSL ou Git Bash no Windows):

```bash
make format && make check     # ruff, mypy, lint-imports, pytest com cobertura
make openapi                  # se o contrato HTTP mudou
```

Sem `make`, com o venv ativado (`source .venv/bin/activate` no Linux/macOS, `source .venv/Scripts/activate` no Git Bash, `.venv\Scripts\Activate.ps1` no PowerShell — criar/instalar em [docs/11](../docs/11-comandos.md)):

```bash
ruff format . && ruff check --fix .
mypy api tests
lint-imports
coverage run -m pytest && coverage report
python -m api.scripts.export_openapi openapi.json   # se o contrato HTTP mudou
```

Sem ambiente Python local, pela imagem de dev (`docker compose -f docker-compose.dev.yml build bot-varejo-api` uma vez):

```bash
docker run --rm -u "$(id -u):$(id -g)" -e HOME=/tmp -v "$PWD":/app -w /app bot-varejo-api:dev \
  sh -c 'ruff format . && ruff check --fix . && mypy api tests && lint-imports && coverage run -m pytest && coverage report'
```

## Documentação

Toda mudança de comportamento atualiza os docs no mesmo MR: endpoint/mensagem nova em `docs/06-contratos-api.md` + `openapi.json`; context novo em `docs/01-arquitetura.md` (evolução) quando aplicável; lib nova em `docs/13-dependencias.md`. Docs descrevem só o estado atual. Regras de escrita em [docs.instructions.md](instructions/docs.instructions.md); tarefas só de documentação usam o agente [docs-backend](agents/docs-backend.agent.md) (`/documentar`, `/novo-adr`, `/revisar-docs`). O teste `tests/contract/test_docs.py` valida links e trechos de código dos docs.

## Commits

Formato `tipo: [CPBS-<n>] descrição` em pt-BR (ex.: `feat: [CPBS-123] adiciona health check por escopo`) — ver [CONTRIBUTING.md](../CONTRIBUTING.md). Nunca faça commit, push ou tag sem o desenvolvedor pedir.
