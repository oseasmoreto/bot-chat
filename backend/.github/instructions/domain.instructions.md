---
applyTo: "api/contexts/**/domain/**"
description: "Camada domain de um bounded context: Python puro, entidades, value objects, ports e exceções de negócio"
---

# Camada `domain`

Regras de negócio em **Python puro**. Referência: `api/contexts/health/domain/`.

- Pode importar: stdlib, `api.core.scope`, `api.core.exceptions` e o próprio domínio do context.
- **Proibido** (quebra o import-linter): FastAPI, Pydantic, Starlette, boto3/aioboto3/botocore, httpx, tenacity e qualquer import de `application`, `infrastructure`, `presentation` ou de outro context.
- Arquivos:
  - `entities.py` — entidades e agregados: `@dataclass(frozen=True, slots=True, kw_only=True)`. Mudança de estado devolve nova instância (`dataclasses.replace`) e valida invariantes.
  - `value_objects.py` — tipos pequenos e imutáveis (`StrEnum`, dataclass frozen, `NewType` para ids como `PartnerId`).
  - `ports.py` — interfaces para o mundo externo como `typing.Protocol`: `<Entidade>Repository` (persistência) e `<Nome>Port` (relógio, APIs de parceiros). Métodos de I/O são `async`. Ports pequenas e específicas.
  - `errors.py` — exceções de negócio herdando de `DomainError`, `NotFoundError` ou `ConflictError` (`api.core.exceptions`), com `code` snake_case estável e `status_code` quando não for 422:

    ```python
    from http import HTTPStatus

    from api.core.exceptions import DomainError


    class PartnerInactiveError(DomainError):
        code = "partner_inactive"
        status_code = HTTPStatus.UNPROCESSABLE_ENTITY
    ```

- Entidades persistidas com locking otimista têm `version: int`.
- Datas sempre com fuso (UTC); a hora atual vem de uma `ClockPort`, nunca de `datetime.now()` no domínio.
- Sem I/O, sem logging, sem leitura de configuração.
- Todo comportamento tem teste unitário em `tests/unit/contexts/<ctx>/domain/`.
