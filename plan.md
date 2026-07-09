# Project Plan - GitHub Data Pipeline API

> Projeto desenvolvido para a disciplina de Engenharia de Dados, DevOps e IA Aplicada, utilizando uma arquitetura baseada em ETL, APIs REST e boas práticas de desenvolvimento moderno em Python.

---

# 🎯 Objetivo

Desenvolver um pipeline completo de Engenharia de Dados capaz de consumir informações públicas da GitHub API, realizar tratamento e enriquecimento dos dados, persisti-los em um banco PostgreSQL e disponibilizá-los através de uma API REST desenvolvida com FastAPI.

O projeto seguirá os mesmos princípios arquiteturais do projeto de referência da disciplina, adaptando a implementação para o ecossistema Python e incorporando ferramentas modernas como Prefect para orquestração e Alembic para versionamento do banco de dados.

---

# Objetivos Específicos

- Consumir dados públicos da GitHub API.
- Implementar boas práticas de coleta de dados.
- Tratar e normalizar os dados obtidos.
- Persistir apenas informações relevantes.
- Criar uma API REST para consulta dos dados.
- Orquestrar todo o pipeline utilizando Prefect.
- Versionar o banco utilizando Alembic.
- Containerizar toda aplicação utilizando Podman.
- Automatizar CI/CD utilizando GitHub Actions.

---

# Requisitos Funcionais

## RF001

Consumir dados da GitHub API.

---

## RF002

Persistir usuários do GitHub.

---

## RF003

Persistir repositórios públicos.

---

## RF004

Executar pipeline completo de ingestão.

---

## RF005

Disponibilizar API REST para consulta.

---

## RF006

Permitir reprocessamento do pipeline.

---

## RF007

Exibir status da sincronização.

---

# Requisitos Não Funcionais

- Python 3.13
- FastAPI
- PostgreSQL
- SQLAlchemy 2.x
- Alembic
- Prefect
- Podman
- GitHub Actions
- Pytest
- Ruff
- Black
- Pydantic Settings
- HTTPX

---

# Arquitetura

```
                GitHub API
                     │
                     ▼
             Prefect Flow
        ┌─────────────────────┐
        │ Extract             │
        │ Validate            │
        │ Transform           │
        │ Enrichment          │
        │ Load                │
        └──────────┬──────────┘
                   │
                   ▼
             PostgreSQL
                   │
          SQLAlchemy ORM
                   │
                   ▼
             FastAPI REST
                   │
                   ▼
               Cliente
```

---

# Arquitetura do Projeto

```
.
├── .github/
│   └── workflows/
│
├── config/
│
├── docs/
│   └── adr/
│
├── k8s/
│
├── scripts/
│
├── src/
│   ├── api/
│   ├── core/
│   ├── database/
│   ├── integrations/
│   ├── jobs/
│   ├── prefect/
│   ├── repositories/
│   ├── routers/
│   ├── schemas/
│   ├── services/
│   ├── models/
│   ├── utils/
│   └── main.py
│
├── tests/
│
├── alembic/
│
├── compose.yaml
├── Containerfile
├── Makefile
├── pyproject.toml
└── README.md
```

---

# Stack Tecnológica

| Tecnologia | Finalidade |
|------------|------------|
| Python | Linguagem principal |
| FastAPI | API REST |
| PostgreSQL | Banco de Dados |
| SQLAlchemy | ORM |
| Alembic | Migrações |
| Prefect | Orquestração ETL |
| Podman | Containers |
| Podman Compose | Orquestração local |
| GitHub Actions | CI/CD |
| HTTPX | Cliente HTTP |
| Ruff | Linter |
| Black | Formatação |
| Pytest | Testes |

---

# Fluxo de Dados

```
GitHub API

↓

Extração

↓

Validação

↓

Transformação

↓

Enriquecimento

↓

Carga PostgreSQL

↓

API REST
```

---

# Engenharia de Dados

A aplicação não armazenará todos os dados retornados pela GitHub API.

Será realizada uma etapa de transformação para persistir apenas as informações relevantes ao domínio da aplicação.

## Dados coletados

### Usuários

- id
- login
- nome
- seguidores
- seguindo
- quantidade de repositórios
- data de criação

### Repositórios

- id
- nome
- linguagem
- estrelas
- forks
- issues abertas
- data de criação
- última atualização

---

# Enriquecimento de Dados

Além dos dados fornecidos pela API serão criadas métricas derivadas.

Exemplos:

- Followers por repositório
- Score de popularidade
- Idade da conta
- Repositórios por ano
- Linguagem principal
- Média de estrelas por repositório

Essas métricas caracterizam a etapa de Engenharia de Dados do projeto.

---

# Banco de Dados

## users

| Campo |
|--------|
| id |
| github_id |
| login |
| name |
| followers |
| following |
| public_repos |
| account_created_at |
| created_at |
| updated_at |

---

## repositories

| Campo |
|--------|
| id |
| github_repo_id |
| name |
| language |
| stars |
| forks |
| open_issues |
| owner_id |
| created_at |
| updated_at |

---

## pipeline_execution

Tabela responsável pelo controle das execuções do pipeline.

Campos:

- id
- execution_date
- pipeline
- status
- records_processed
- execution_time
- error_message

---

# ORM

Será utilizado SQLAlchemy 2.x para:

- Mapeamento ORM
- Relacionamentos
- Consultas
- Repositórios
- Persistência

---

# Versionamento do Banco

Será utilizado Alembic.

Objetivos:

- Controle de versões
- Migrações
- Rollback
- Evolução do Schema

Fluxo:

```
Model

↓

Alembic Revision

↓

Migration

↓

Banco atualizado
```

---

# Integração com GitHub API

A integração ficará isolada.

```
src/

integrations/

github/

client.py

users.py

repositories.py
```

Essa abordagem facilita futuras integrações com outras APIs públicas.

---

# Pipeline ETL

## Extract

Responsável pela coleta dos dados na GitHub API.

---

## Validate

Validação de:

- tipos
- dados obrigatórios
- duplicidades

---

## Transform

Aplicação das regras de negócio.

Exemplo:

- remoção de atributos
- normalização
- padronização

---

## Enrichment

Criação de métricas derivadas.

---

## Load

Persistência no PostgreSQL.

---

# Orquestração

Será utilizado Prefect.

Fluxo:

```
github_pipeline

↓

extract_users

↓

extract_repositories

↓

validate

↓

transform

↓

enrichment

↓

load_database
```

Cada etapa será uma Task independente.

Benefícios:

- Retry automático
- Logs
- Monitoramento
- Reprocessamento
- Observabilidade

---

# API REST

## Endpoints Administrativos

```
POST /admin/extract

POST /admin/transform

POST /admin/load

POST /admin/run-pipeline

GET /admin/status
```

---

## Endpoints Públicos

```
GET /users

GET /users/{login}

GET /repositories

GET /repositories/{id}

GET /statistics

GET /health
```

---

# Containers

A aplicação será executada utilizando Podman.

Serviços:

- API
- PostgreSQL
- Prefect Server
- Prefect Worker
- PgAdmin

---

# CI/CD

Será utilizado GitHub Actions.

Pipeline:

```
Push

↓

Lint

↓

Testes

↓

Coverage

↓

Build

↓

Migrações

↓

Deploy
```

---

# Makefile

Principais comandos.

```bash
make up

make down

make logs

make migrate

make revision

make extract

make transform

make load

make prefect

make test

make lint

make format
```

---

# ADRs

Serão documentadas as principais decisões arquiteturais.

## ADR 0001

Utilização do Podman.

---

## ADR 0002

Utilização do FastAPI.

---

## ADR 0003

Utilização do PostgreSQL.

---

## ADR 0004

Utilização do Prefect.

---

## ADR 0005

Utilização do SQLAlchemy + Alembic.

---

## ADR 0006

Integração com GitHub API.

---

# Estrutura das Camadas

```
Routers

↓

Services

↓

Repositories

↓

Database
```

Separação de responsabilidades:

- Router → Endpoints
- Service → Regras de negócio
- Repository → Persistência
- Database → ORM

---

# Testes

Serão implementados:

- Testes Unitários
- Testes de Integração
- Testes End-to-End

Ferramenta:

- Pytest

---

# Boas Práticas

- SOLID
- Clean Architecture (adaptada)
- Repository Pattern
- Service Layer
- Dependency Injection
- Tipagem estática
- Configuração por ambiente
- Logs estruturados
- Versionamento do banco
- Documentação automática (Swagger/OpenAPI)
- Testes automatizados
- CI/CD

---

# Roadmap

## Sprint 1

- Estrutura inicial
- FastAPI
- PostgreSQL
- SQLAlchemy
- Alembic
- Podman

---

## Sprint 2

- Integração GitHub API
- Extração dos dados
- Persistência

---

## Sprint 3

- Pipeline Prefect
- ETL completo
- Controle das execuções

---

## Sprint 4

- API REST
- Paginação
- Filtros
- Estatísticas

---

## Sprint 5

- GitHub Actions
- Testes
- Documentação
- Refatoração

---

# Critérios de Aceite

- Consumir dados públicos da GitHub API.
- Persistir apenas informações relevantes.
- Utilizar SQLAlchemy como ORM.
- Versionar banco com Alembic.
- Orquestrar o pipeline utilizando Prefect.
- Containerizar a aplicação utilizando Podman.
- Implementar CI/CD com GitHub Actions.
- Disponibilizar documentação automática da API.
- Possuir testes automatizados.
- Seguir boas práticas de Engenharia de Dados e DevOps.

---

# Melhorias Futuras

- Cache com Redis.
- Observabilidade com Prometheus e Grafana.
- Deploy em Kubernetes.
- Versionamento de dados com DVC.
- Integração com MLflow.
- Dashboard analítico com Metabase.
- Agendamento automático dos fluxos do Prefect.
- Suporte a múltiplas APIs públicas.