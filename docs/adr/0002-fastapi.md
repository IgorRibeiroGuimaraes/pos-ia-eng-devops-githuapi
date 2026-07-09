# ADR 0002 — Utilização do FastAPI

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O projeto necessita de uma camada de API REST para expor os dados processados pelo pipeline ETL.

## Decisão

Utilizar **FastAPI** como framework web.

## Justificativa

- Geração automática de documentação OpenAPI/Swagger em `/docs`.
- Validação de entrada e serialização via **Pydantic v2** nativa.
- Suporte a tipagem estática e async/await.
- Alta performance (Starlette + Uvicorn).
- Injeção de dependência integrada (`Depends`), facilitando testes e desacoplamento.

## Consequências

- Pydantic v2 como camada de validação e serialização.
- Uvicorn como servidor ASGI.
- Schemas separados dos modelos ORM.
