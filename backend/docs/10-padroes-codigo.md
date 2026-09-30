# 10 — Padrões de código

## Nomenclatura: Python × contrato

A orientação do projeto é **camelCase para métodos**. No backend aplicamos assim ([ADR-0005](./adr/0005-convencao-de-nomes.md)):

- **Código Python:** segue a **PEP 8** (`snake_case` em funções/métodos), padrão da linguagem e exigido pelo `ruff` (regra `N802`). camelCase no Python iria contra FastAPI, Pydantic e a stdlib.
- **Contrato (JSON da API, mensagens WS, operationId):** **camelCase**. A conversão é automática via `BaseSchema` — o frontend só enxerga camelCase.

## Convenções da API e das mensagens

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Campo JSON | camelCase | `uptimeSeconds` |
| Path | kebab-case, plural | `/api/v1/admin/partner-services` |
| operationId | camelCase | `getAdminHealth` |
| Tipo de mensagem WS | `contexto.acao` minúsculo | `health.ping` |
| Código de erro | snake_case | `unknown_message_type` |

## Boas práticas gerais

- **Funções pequenas** com uma responsabilidade; se precisa de "e" para descrever, divida.
- **Early return** em vez de `if` aninhado.
- **Sem números/strings mágicos**: constantes nomeadas.
- **Imutabilidade por padrão** (`frozen=True`, `readonly`, `as const`).
- **Comentários explicam o porquê**, não o quê. Código auto-explicativo dispensa comentário.
- **Sem código morto** nem comentado — o git guarda o histórico.
- **Sem segredos no código** — variáveis de ambiente; `.env` nunca é commitado.
- Textos da interface em **pt-BR**; código (nomes) em **inglês**.

## Formatação e lint

| Ferramenta | Config |
|------------|--------|
| `ruff format` | `line-length = 100` |
| `ruff check` | regras na seção `pyproject.toml` abaixo |
| `mypy` | `strict = true` |
| `import-linter` | fronteiras das camadas DDD ([03](./03-arquitetura-ddd.md)) |
| EditorConfig | UTF-8, LF, indentação 4, newline final |
| pre-commit | roda ruff e mypy nos arquivos alterados |


## Nomenclatura do código Python

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Função, método, variável | snake_case | `execute`, `build_health_router` |
| Classe | PascalCase | `GetHealthUseCase`, `HealthReport` |
| Caso de uso | `<Verbo><Substantivo>UseCase` | `GetHealthUseCase` |
| Port (Protocol) | `<Nome>Port` | `ClockPort` |
| Adapter | nome da tecnologia/implementação | `SystemClock`, `DynamoDbPartnerRepository` |
| Schema de saída | `<Nome>Response` | `HealthResponse` |
| Schema de entrada | `<Nome>Request` | `CreateFlowRequest` |
| Constante | UPPER_SNAKE_CASE | `STARTED_AT` |
| Privado | prefixo `_` | `self._clock` |
| Módulo / pacote | snake_case | `get_health.py`, `system_clock.py` |
| Teste | `test_<comportamento>` | `test_returns_ok_when_there_are_no_checks` |

## Tipagem

- `mypy --strict` sem exceções globais
- Toda função com anotação de parâmetros e retorno (ruff `ANN`)
- `typing.Protocol` para ports
- `@dataclass(frozen=True, slots=True)` para objetos de domínio
- `Any` apenas na fronteira (payload WS) e documentado
- `# type: ignore` exige código e justificativa: `# type: ignore[arg-type]  # motivo`

## Boas práticas específicas do backend

- `async def` em toda rota e caso de uso; nada bloqueante no event loop (ruff `ASYNC` ajuda).
- Nada de FastAPI/Pydantic dentro de `domain/`.
- Injeção de dependência pelo construtor (casos de uso) e por `Depends` (presentation).
- Exceções de domínio com `code` estável; nunca retornar stack trace.

## Configuração das ferramentas (`pyproject.toml`)

O `pyproject.toml` só configura as ferramentas; as dependências ficam em `requirements.txt` e `requirements-test.txt`, com versões fixadas ([ADR-0004](./adr/0004-pip-requirements.md)).

```toml
# Configuração das ferramentas. As dependências ficam em requirements.txt / requirements-test.txt.
[project]
name = "bot-varejo"
version = "0.1.0"
requires-python = ">=3.13"

[tool.ruff]
line-length = 100
target-version = "py313"
src = ["."]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM", "ASYNC", "RUF", "ANN", "S", "PT", "PL"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "PLR2004", "PLR0913", "PLR0917"]   # assert, números mágicos e fixtures

[tool.mypy]
strict = true
plugins = ["pydantic.mypy"]

[tool.pytest.ini_options]
asyncio_mode = "auto"
asyncio_default_fixture_loop_scope = "function"
testpaths = ["tests"]
pythonpath = ["."]                 # `import api...` e `from tests.fakes import ...`
addopts = "--strict-markers --strict-config"
filterwarnings = [
    "error",
    # Aviso interno do Starlette com o anyio atual; não vem do nosso código.
    "ignore:The anyio.abc.BlockingPortal alias is deprecated:DeprecationWarning",
]

[tool.coverage.run]
source = ["api"]
branch = true

[tool.coverage.report]
fail_under = 90
show_missing = true
skip_covered = true
exclude_also = [
    "class .*\\bProtocol\\):",    # ports: só assinaturas
    "if __name__ == .__main__.:",
]

[tool.importlinter]
root_packages = ["api"]
include_external_packages = true   # necessário para proibir fastapi/pydantic/boto no domínio

[[tool.importlinter.contracts]]
name = "Camadas de cada context"
type = "layers"
containers = ["api.contexts.*"]            # todo context novo entra sozinho
layers = ["presentation", "application", "domain"]

[[tool.importlinter.contracts]]
name = "Presentation não importa infrastructure diretamente (só via container)"
type = "forbidden"
source_modules = ["api.contexts.*.presentation"]
forbidden_modules = ["api.contexts.*.infrastructure"]
allow_indirect_imports = true

[[tool.importlinter.contracts]]
name = "Domínio não depende de frameworks nem de AWS"
type = "forbidden"
source_modules = ["api.contexts.*.domain"]
forbidden_modules = [
    "fastapi", "pydantic", "starlette", "aioboto3", "boto3", "botocore", "httpx", "tenacity",
]

[[tool.importlinter.contracts]]
name = "Casos de uso não dependem de framework web, AWS nem HTTP (usam as ports)"
type = "forbidden"
source_modules = ["api.contexts.*.application"]
forbidden_modules = ["fastapi", "starlette", "aioboto3", "boto3", "botocore", "httpx"]

[[tool.importlinter.contracts]]
name = "Contexts independentes entre si"
type = "independence"
modules = ["api.contexts.*"]
```
