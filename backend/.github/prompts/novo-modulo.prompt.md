---
description: "Adiciona um módulo (funcionalidade) a um context existente: análise, caso de uso, ports/adapters e exposição HTTP/WS"
agent: backend-ddd
argument-hint: "context e funcionalidade (ex.: partners — desativar parceiro)"
---

No context **${input:context:context existente, ex.: partners}**, adicione a funcionalidade: ${input:funcionalidade:o que o módulo faz, regras e quem usa (public/admin)}

Siga o [agente backend-ddd](../agents/backend-ddd.agent.md) — fases **Análise → Plano → Construção → Validação** — e as instruções em `.github/instructions/`.

## Fase 1 — Roteiro específico (além do roteiro comum do agente)

Leia primeiro todo o context (`api/contexts/<context>/`) e responda sozinho o que ele já define.

**Encaixe no context**
- [ ] A funcionalidade pertence mesmo a este context, ou a outro/novo? (se não pertencer, pare e aponte)
- [ ] Reaproveita quais entidades, value objects, ports e schemas existentes? O que é novo?
- [ ] Muda uma entidade existente (campo novo, estado novo, transição nova)? Registros já persistidos precisam de valor padrão ou `schemaVersion` novo?

**Regras**
- [ ] Quais invariantes novas ou alteradas? Em que estados a operação é permitida?
- [ ] Efeitos colaterais: altera outros dados, dispara notificação/integração, afeta outro context?
- [ ] O que acontece se executada duas vezes (idempotência) ou ao mesmo tempo por dois usuários (concorrência)?

**Exposição**
- [ ] Novo endpoint, nova mensagem WS, ou só uso interno por outro caso de uso? (para endpoint/mensagem, siga também o roteiro de `/novo-endpoint` ou `/nova-mensagem-ws`)
- [ ] Muda a resposta de algo já exposto? É compatível com o frontend atual?

## Passos

1. Teste primeiro: unitário do caso de uso (com fakes) e, se exposto, integração da rota/mensagem — um por critério de aceite.
2. Domínio: regras novas na entidade/value object; erro de negócio novo em `domain/errors.py`; port nova só se precisar de algo externo novo.
3. Caso de uso em `application/<verbo>_<substantivo>.py` (`<Verbo><Substantivo>UseCase.execute`).
4. Adapter para port nova em `infrastructure/`.
5. Exposição: endpoint em `presentation/http.py` e/ou handler em `presentation/ws_handlers.py`; schemas em `presentation/schemas.py`; provider em `presentation/dependencies.py`.
6. Composição: `api/container.py` (+ `dispatcher.register` para WS).
7. Contrato: `openapi.json` regenerado e `docs/06-contratos-api.md` atualizado; termos novos no glossário.
8. Validação completa e resumo final.
