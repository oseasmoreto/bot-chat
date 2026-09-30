---
applyTo: "tests/**"
description: "Testes do backend: TDD, pytest async, fakes das ports, integração HTTP/WebSocket, contrato OpenAPI"
---

# Testes

Referência: `tests/` e [docs/09 — Testes](../../docs/09-testes.md).

- **TDD**: o teste vem antes do código de produção e entra no mesmo MR. Toda rota, mensagem WS e caso de uso tem teste; cobertura ≥ 90% (linhas e branches).
- Estrutura espelha `api/`: `tests/unit/contexts/<ctx>/{domain,application}/`, `tests/unit/core/`, `tests/integration/api/`, `tests/integration/websocket/`, `tests/integration/contexts/<ctx>/` (adapters com DynamoDB Local), `tests/contract/`. Toda pasta com `__init__.py`.
- Nome: arquivo `test_<modulo>.py`; função `test_<comportamento>_when_<condição>`; Arrange / Act / Assert separados por linha em branco; sem lógica (`if`/loops) no teste — use `@pytest.mark.parametrize`.
- Testes `async def` rodam sozinhos (`asyncio_mode = "auto"`), sem marcador.
- Dublês: *fakes* que implementam as ports em `tests/fakes.py` (ex.: `FakeClock`, `StubCheck`, `InMemoryPartnerRepository`). `mocker` (pytest-mock) só na fronteira com libs externas; nunca `mock.patch` no domínio.
- Relógio: `FakeClock` no domínio/casos de uso; `freezegun` só quando o código lê a hora direto (ex.: logs).
- Fixtures prontas em `tests/conftest.py`: `settings`, `app`, `client` (httpx `AsyncClient`), `ws_client` (`TestClient`), `ALLOWED_ORIGIN`. Substitua casos de uso com `app.dependency_overrides[get_<caso>] = lambda: fake`.
- Rotas: testar status, corpo em camelCase, os dois escopos quando existirem e cada erro esperado (`{"error": {"code": ...}}`).
- WebSocket: sempre com `headers={"origin": ALLOWED_ORIGIN}`; testar resposta, `id` repetido e payload inválido.
- HTTP externo: `httpx.MockTransport`, nunca rede real.
- `filterwarnings = error`: não silencie avisos no teste; corrija a causa.
