# ADR 0003 — Utilização do PostgreSQL

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O projeto necessita de um banco de dados relacional para persistir usuários, repositórios e execuções do pipeline.

## Decisão

Utilizar **PostgreSQL 16** como banco de dados.

## Justificativa

- Suporte a `RETURNING *` em INSERT/UPDATE, eliminando queries extras após escrita.
- Tipos avançados (JSONB, arrays, timezone-aware timestamps).
- Robusto, open-source e amplamente suportado em ambientes cloud.
- Compatibilidade total com SQLAlchemy e Alembic.

## Consequências

- Queries SQL utilizam sintaxe PostgreSQL (`RETURNING`, `NOW()`, etc.).
- Não há compatibilidade garantida com outros bancos sem ajuste nas queries raw.
