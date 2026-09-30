---
applyTo: "api/contexts/**/application/**"
description: "Camada application: um caso de uso por arquivo, orquestrando domínio e ports"
---

# Camada `application` (casos de uso)

Referência: `api/contexts/health/application/get_health.py`.

- **Um caso de uso por arquivo**, nome do arquivo em snake_case do verbo + substantivo (`create_partner.py`) e classe `<Verbo><Substantivo>UseCase` (`CreatePartnerUseCase`).
- Dependências **só por construtor, keyword-only**, tipadas pelas ports do domínio (nunca por classes concretas):

  ```python
  class CreatePartnerUseCase:
      def __init__(self, *, partners: PartnerRepository, clock: ClockPort) -> None:
          self._partners = partners
          self._clock = clock

      async def execute(self, command: CreatePartnerCommand) -> Partner: ...
  ```

- Método público único: `async def execute(...)`. Entrada com vários campos = dataclass frozen `<Verbo><Substantivo>Command` (ou `…Query` para leitura) no mesmo arquivo; saída = entidade/objeto do domínio (nunca schema Pydantic).
- Orquestra: busca pelas ports, aplica regras do domínio, persiste, devolve. Regra de negócio mora no domínio, não aqui.
- Erros de negócio: levantar exceções do `domain/errors.py` do context (ou `NotFoundError`/`ConflictError` de `api.core.exceptions`).
- Pode importar: `domain` do próprio context, `api.core` puro (`scope`, `exceptions`). **Proibido** (import-linter): FastAPI, Starlette, boto3/aioboto3/botocore, httpx, `infrastructure`, `presentation`.
- O caso de uso é exposto igual para HTTP e WebSocket — nada de lógica duplicada nos handlers.
- Registrar a instância em `api/container.py` (campo no `Container` + montagem em `build_container`).
- Teste unitário obrigatório em `tests/unit/contexts/<ctx>/application/test_<arquivo>.py`, com *fakes* das ports (adicione os fakes em `tests/fakes.py`).
