# ADR 0006 — Integração com GitHub API

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O projeto precisa consumir dados públicos da GitHub API de forma organizada e extensível.

## Decisão

Isolar a integração em `src/integrations/github/` com client, módulo de usuários e módulo de repositórios separados.

## Justificativa

- Isolamento facilita mock nos testes e substituição futura por outras APIs.
- `httpx` como cliente HTTP: suporte a sync e async, timeouts configuráveis.
- Token de autenticação via `Authorization: Bearer` aumenta o rate limit de 60 para 5.000 req/h.
- Estrutura espelhável para outras integrações (`src/integrations/gitlab/`, etc.).

## Consequências

- `GITHUB_TOKEN` no `.env` é opcional, mas recomendado para evitar rate limit.
- A etapa de extração faz uma query de busca + N queries individuais de usuário (N+1 controlado).
- Retry é gerenciado pelo Prefect nas tasks de extração.
