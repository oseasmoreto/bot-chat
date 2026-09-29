# 03 — Arquitetura DDD

## Organização: DDD com bounded contexts

Cada **bounded context** (`contexts/<nome>/`) é um módulo autocontido com quatro camadas. O primeiro context é `health`. Os próximos (`conversation`, `flows`, `integrations`, `partners`, `identity`) seguem o mesmo molde — ver [01 — Arquitetura, evolução prevista](./01-arquitetura.md#6-evolução-prevista-não-implementar-agora).

```mermaid
flowchart TB
    subgraph ctx["contexts/health"]
        direction TB
        P["presentation<br/>routers HTTP, handlers WS, schemas Pydantic"]
        A["application<br/>casos de uso (orquestração)"]
        D["domain<br/>entidades, value objects, ports — Python puro"]
        I["infrastructure<br/>adapters que implementam as ports"]
        P --> A --> D
        I -. "implementa ports" .-> D
    end
    core["core/ (shared kernel)<br/>config, logging, errors, Scope, BaseSchema, WS dispatcher"]
    api["api/ (composição por escopo)<br/>public.py, admin.py, websocket.py"]
    main["main.py + container.py<br/>(composition root)"]

    api --> P
    main --> api
    main --> I
    P --> core
    A --> core
```

### Responsabilidade de cada camada

| Camada | Pode importar | Não pode importar | Conteúdo |
|--------|---------------|-------------------|----------|
| `domain` | stdlib, `core.scope` | FastAPI, Pydantic, `application`, `infrastructure`, `presentation` | Entidades, value objects, regras de negócio, *ports* (`typing.Protocol`) |
| `application` | `domain`, `core` | FastAPI, `infrastructure`, `presentation` | Casos de uso: orquestram domínio + ports. Uma classe = um caso de uso |
| `infrastructure` | `domain`, `core`, libs externas | `presentation` | Implementações concretas das ports (relógio, repositórios DynamoDB, HTTP de parceiros…) |
| `presentation` | `application`, `domain`, `core`, FastAPI | `infrastructure` diretamente | Routers, schemas de entrada/saída, handlers WS, conversão domínio ⇄ DTO |
| `api/` | `presentation` de todos os contexts | — | Agrupa routers por escopo (`public`/`admin`) e define prefixos |
| `main.py` / `container.py` | tudo | — | **Composition root**: instancia adapters e injeta nos casos de uso |

Essas fronteiras serão verificadas automaticamente com **import-linter** (contratos em `pyproject.toml`) no CI.

```toml
# pyproject.toml (trecho)
[tool.importlinter]
root_package = "bot_varejo"

[[tool.importlinter.contracts]]
name = "Camadas de cada context"
type = "layers"
containers = ["bot_varejo.contexts.health"]
layers = ["presentation", "application", "domain"]

[[tool.importlinter.contracts]]
name = "Domínio não depende de frameworks nem de AWS"
type = "forbidden"
source_modules = ["bot_varejo.contexts.health.domain"]
forbidden_modules = ["fastapi", "pydantic", "starlette", "aioboto3", "boto3", "botocore"]
```

## Aplicação de SOLID, DRY, KISS

| Princípio | Onde aparece |
|-----------|--------------|
| **S** — Single Responsibility | `GetHealthUseCase` só calcula o relatório; `HealthResponse` só serializa; router só traduz HTTP ⇄ caso de uso |
| **O** — Open/Closed | Novas dependências no health = novo `HealthCheckPort` registrado no container, sem alterar o caso de uso. Novas mensagens WS = novo handler registrado no `MessageDispatcher` |
| **L** — Liskov | Qualquer implementação de `ClockPort` (sistema ou fake de teste) é intercambiável |
| **I** — Interface Segregation | Ports pequenas e específicas (`ClockPort.now()`), nada de "god interfaces" |
| **D** — Dependency Inversion | Caso de uso depende de `Protocol`, não de classes concretas; concreto injetado no composition root |
| **DRY** | `build_health_router(scope)` gera o mesmo router para `public` e `admin`; `BaseSchema` centraliza a config camelCase |
| **KISS** | Sem framework de DI, sem ORM, sem event bus enquanto não forem necessários — um `Container` dataclass resolve |
