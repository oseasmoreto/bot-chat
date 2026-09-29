# Backend — Padrões de código Python

> Padrões transversais (API, formatação geral) em [06 — Padrões gerais](../06-padroes-gerais.md). Por que Python usa `snake_case`: [ADR-0008](../adr/0008-convencao-de-nomes.md).

## Nomenclatura

| Elemento | Convenção | Exemplo |
|----------|-----------|---------|
| Função, método, variável | snake_case | `execute`, `build_health_router` |
| Classe | PascalCase | `GetHealthUseCase`, `HealthReport` |
| Caso de uso | `<Verbo><Substantivo>UseCase` | `GetHealthUseCase` |
| Port (Protocol) | `<Nome>Port` | `ClockPort` |
| Adapter | nome da tecnologia/implementação | `SystemClock`, `PostgresPartnerRepository` |
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

## Boas práticas

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
