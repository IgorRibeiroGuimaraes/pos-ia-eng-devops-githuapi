# ADR 0005 — SQLAlchemy + Alembic (SQL-first)

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O projeto necessita de mapeamento de banco de dados e versionamento de schema.

## Decisão

Utilizar **SQLAlchemy 2.x** para definição dos modelos e **Alembic** para migrações, com abordagem **SQL-first** nas queries.

## Justificativa

- Os modelos ORM existem exclusivamente para o Alembic gerar migrações via `autogenerate`.
- Todas as queries usam `text()` com SQL raw parametrizado — sem uso de ORM session queries.
- Essa abordagem dá controle total sobre o SQL gerado e facilita otimizações.
- Parâmetros nomeados (`:param`) previnem SQL injection via prepared statements.
- Colunas dinâmicas em UPDATE são validadas contra whitelist antes de compor o SQL.

## Consequências

- Repositórios retornam `dict` em vez de instâncias de modelo.
- `from_attributes=True` nos schemas Pydantic é mantido para compatibilidade futura.
- Qualquer novo campo no modelo ORM deve ser refletido manualmente nas queries dos repositórios.
