---
description: "Revisa a documentação do backend contra o código e as regras de documentação (só relatório, sem alterar arquivos)"
agent: docs-backend
argument-hint: "(opcional) docs ou assunto para focar"
---

Revise a documentação do backend ${input:foco:(opcional) docs ou assunto para focar}.

Não altere nada nesta etapa (a fase de Análise do agente é dispensada): produza um relatório em pt-BR, do mais grave para o menos grave, com arquivo:linha, problema e correção sugerida. Verifique:

1. **Docs × código:** endpoints, mensagens WS, erros, variáveis, estrutura de pastas, comandos e libs descritos batem com o código atual? Trechos de código embutidos iguais aos arquivos?
2. **Estado atual:** há histórico, "antes/agora", decisões revogadas, ferramentas anteriores ou propostas descartadas?
3. **Regras de conteúdo:** docs permanentes citando tarefas; menção a outros repositórios além do frontend; CI/CD, pipelines, deploy automatizado, hooks de commit ou tutoriais de configuração do GitLab.
4. **ADRs:** formato, uma decisão por ADR, alternativas só não adotadas, índice atualizado.
5. **Estrutura:** índice `docs/README.md` completo, glossário com os termos usados, `docs/02-estrutura.md` igual à árvore real.
6. **Comandos:** funcionam na raiz do projeto e cobrem Linux/macOS/WSL, Git Bash e PowerShell quando diferem; commits de exemplo no formato `tipo: [CPBS-123] descrição`.
7. **Diagramas Mermaid:** sintaxe conforme [docs.instructions.md](../instructions/docs.instructions.md#diagramas-mermaid).
8. **Instruções do Copilot** (`.github/`) coerentes com os docs.

Rode `coverage run -m pytest tests/contract` (ou `make check`) e inclua o resultado no relatório.
