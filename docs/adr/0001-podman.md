# ADR 0001 — Utilização do Podman em vez do Docker

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O projeto necessita de containerização para garantir portabilidade e consistência entre ambientes de desenvolvimento, CI e produção.

## Decisão

Utilizar **Podman** como runtime de containers no lugar do Docker.

## Justificativa

- Podman é **daemonless** — não requer um processo central em execução, reduzindo superfície de ataque.
- Opera por padrão em modo **rootless**, seguindo o princípio de menor privilégio.
- Compatível com imagens OCI e com a sintaxe do Dockerfile (renomeado para `Containerfile` por convenção Podman).
- Disponível nativamente no ambiente de desenvolvimento utilizado (Windows com Podman Desktop).

## Consequências

- `Containerfile` no lugar de `Dockerfile`.
- `podman-compose` no lugar de `docker-compose`.
- CI/CD usa `podman build` no workflow do GitHub Actions.
