# Tarefas — Backend

Registro das tarefas (tickets do Jira) que afetam este projeto: enunciado, objetivo, critérios de aceitação, definição de pronto e fora de escopo.

A documentação permanente (`docs/`, ADRs, READMEs) descreve **o que o sistema é**, sem referência a tarefas. O que é específico de uma entrega fica aqui.

| Ticket | Título | Status |
|--------|--------|--------|
| [CPBS-275](./CPBS-275-fundacao.md) | Fundação do projeto | Backend implementado · integração com o frontend pendente |

## Como registrar uma tarefa

1. Criar `CPBS-<numero>-<slug>.md` nesta pasta, com: enunciado, objetivo neste projeto, **análise** (perguntas feitas, respostas e tabela de decisões — o agente `backend-ddd` gera esta seção, ver [14 — IA](../14-ia-copilot.md#3-análise-antes-de-construir)), critérios de aceitação (apontando para os docs permanentes), definição de pronto, fora de escopo, decisões registradas (ADRs) e entregáveis.
2. Adicionar a linha na tabela acima.
3. Mudanças permanentes (arquitetura, contratos, padrões) vão para `docs/` e ADRs — nunca só aqui.
