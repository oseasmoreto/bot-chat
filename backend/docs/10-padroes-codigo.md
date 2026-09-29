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
| pre-commit | roda ruff e mypy nos arquivos alterados de `backend/` |


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

```toml
[project]
name = "bot-varejo"
version = "0.1.0"
requires-python = ">=3.13"
dependencies = [
    "fastapi",
    "uvicorn[standard]",        # inclui suporte a websockets
    "pydantic",
    "pydantic-settings",
]

[dependency-groups]
dev = ["pytest", "pytest-asyncio", "pytest-cov", "httpx", "mypy", "ruff", "import-linter"]

[tool.ruff]
line-length = 100
target-version = "py313"
src = ["src", "tests"]

[tool.ruff.lint]
select = ["E", "F", "W", "I", "N", "UP", "B", "SIM", "ASYNC", "RUF", "ANN", "S", "PT", "PL"]
ignore = []

[tool.ruff.lint.per-file-ignores]
"tests/**" = ["S101", "PLR2004"]   # assert e números mágicos permitidos em testes

[tool.mypy]
strict = true
plugins = ["pydantic.mypy"]
mypy_path = "src"

[tool.pytest.ini_options]
asyncio_mode = "auto"
testpaths = ["tests"]
pythonpath = ["."]                 # permite `from tests.fakes import ...`
addopts = "--strict-markers --cov=bot_varejo --cov-report=term-missing"

[tool.coverage.report]
fail_under = 90
show_missing = true
```

> Versões exatas das dependências ficam no `uv.lock` (fixadas no momento da implementação).
