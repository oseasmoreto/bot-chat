---
description: "Revisa as mudanças atuais contra as regras de arquitetura, contrato, testes e docs do backend"
agent: backend-ddd
argument-hint: "(opcional) arquivos ou context para focar"
---

Revise as mudanças pendentes do backend (use `git diff` e `git status`) ${input:foco:(opcional) foco da revisão}.

Não altere nada nesta etapa: produza um relatório em pt-BR, do mais grave para o menos grave, com arquivo:linha, problema e correção sugerida. Verifique:

1. **Camadas DDD:** imports proibidos, regra de negócio fora do domínio, acesso a adapter pela presentation, context importando outro context. Rode `lint-imports`.
2. **Contrato:** camelCase via `BaseSchema`, `operation_id`, `summary`, `responses=`, paths plurais em kebab-case, `openapi.json` atualizado, `docs/06-contratos-api.md` coerente.
3. **Erros e logs:** `DomainError` com `code` estável, sem `HTTPException` para regra de negócio, sem stack trace ou dado sensível em resposta/log.
4. **Testes:** todo caso de uso, rota e mensagem WS novos com teste; fakes em vez de mocks no domínio; cobertura ≥ 90%.
5. **Tipagem e estilo:** `mypy --strict`, `ruff`, nomes no padrão, sem código morto/`print`.
6. **Dependências e config:** libs com `==` e documentadas em `docs/13-dependencias.md`; variáveis novas no `Settings`, `.env.example` e `docs/08`.
7. **Docs:** refletem só o estado atual.

Rode a validação completa e inclua o resultado de cada ferramenta no relatório.
