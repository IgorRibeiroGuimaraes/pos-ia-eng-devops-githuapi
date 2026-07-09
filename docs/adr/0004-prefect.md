# ADR 0004 — Utilização do Prefect

**Status:** Aceito  
**Data:** 2026-07-08

## Contexto

O pipeline ETL precisa de orquestração com suporte a retry, logs, monitoramento e reprocessamento.

## Decisão

Utilizar **Prefect 3** como orquestrador do pipeline ETL.

## Justificativa

- Retry automático por task com `retries` e `retry_delay_seconds`.
- UI web para monitoramento de execuções em `http://localhost:4200`.
- Cada etapa do ETL (extract, transform, enrich, load) é uma `@task` independente.
- O pipeline completo é um `@flow`, facilitando reprocessamento pontual.
- Observabilidade integrada sem necessidade de instrumentação manual.

## Consequências

- `src/prefect/flows.py` contém as definições de tasks e flows.
- Prefect Server roda como serviço separado no `compose.yaml`.
- O pipeline pode ser executado diretamente (`python -m src.prefect.flows`) ou via Prefect Worker.
