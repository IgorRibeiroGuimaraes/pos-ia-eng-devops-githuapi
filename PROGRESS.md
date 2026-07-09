# STATUS DO PROJETO — GitHub Data Pipeline API
> Atualizado em: 2026-07-08

---

## ✅ Fase 1 — Base Concluída (Sprint 1)

### Decisão Arquitetural: SQL-first
- Todos os repositórios usam **SQL raw com `text()`** do SQLAlchemy — sem ORM queries
- Retornam `dict` (via `.mappings()`) em vez de instâncias de modelo
- Padrão: `db.execute(text("SELECT ..."), {...}).mappings().first()`
- INSERTs e UPDATEs usam `RETURNING *` do PostgreSQL
- Os modelos SQLAlchemy (`src/models/models.py`) existem **apenas para Alembic** gerar as migrations

### Ambiente Verificado
- Python 3.12.10 (plano pede 3.13 — usar 3.12, sem impacto prático)
- Podman 5.8.3
- Git 2.51.2
- Sem uv/poetry → usando pip + venv

### Arquivos Criados

#### Configuração
- `pyproject.toml` — dependências, black, ruff, pytest
- `.env.example` — variáveis de ambiente de referência
- `.gitignore`
- `alembic.ini`
- `Makefile`
- `Containerfile` (imagem Podman)
- `compose.yaml` (api, postgres, pgadmin, prefect-server, prefect-worker)

#### Source (`src/`)
| Arquivo | Descrição |
|---------|-----------|
| `src/main.py` | App FastAPI com CORS, routers, /health |
| `src/core/config.py` | Settings via pydantic-settings |
| `src/core/logging.py` | Logger estruturado |
| `src/database/session.py` | Engine SQLAlchemy, SessionLocal, get_db |
| `src/models/models.py` | ORM: User, Repository, PipelineExecution |
| `src/schemas/schemas.py` | Pydantic schemas (request/response) |
| `src/repositories/user_repository.py` | CRUD + upsert de User |
| `src/repositories/repository_repository.py` | CRUD + upsert + stats de Repository |
| `src/repositories/pipeline_repository.py` | Controle de execuções do pipeline |
| `src/integrations/github/client.py` | HTTPx client autenticado |
| `src/integrations/github/users.py` | fetch_user, fetch_users_by_query |
| `src/integrations/github/repositories.py` | fetch_user_repositories |
| `src/jobs/transform.py` | transform_user, transform_repository, enrich_user |
| `src/services/pipeline_service.py` | run_pipeline (Extract→Transform→Enrich→Load) |
| `src/routers/users.py` | GET /users, GET /users/{login} |
| `src/routers/repositories.py` | GET /repositories, GET /repositories/{id} |
| `src/routers/statistics.py` | GET /statistics |
| `src/routers/admin.py` | POST /admin/run-pipeline, GET /admin/status |

#### Testes
- `tests/unit/test_health.py` — health check da API
- `tests/unit/test_transform.py` — transform_user, transform_repository, enrich_user

#### CI/CD
- `.github/workflows/ci.yml` — Lint → Tests (com PostgreSQL) → Build container

#### Alembic
- `alembic/env.py` — configurado com modelos e settings
- `alembic/script.py.mako` — template de migrations
- `alembic/versions/` — aguardando primeira migration

---

## 🔲 Próximas Fases

### Fase 2 — Primeira Migration + Instalação Local
1. Criar `.env` a partir de `.env.example`
2. Subir PostgreSQL: `podman-compose -f compose.yaml up -d postgres`
3. Instalar deps: `pip install -e ".[dev]"`
4. Gerar migration inicial: `alembic revision --autogenerate -m "initial"`
5. Aplicar migration: `alembic upgrade head`
6. Rodar API local: `uvicorn src.main:app --reload`
7. Testar: `pytest`

### Fase 3 — Orquestração com Prefect
- Criar `src/prefect/flows.py` com `@flow` e `@task`
- Registrar deploy no Prefect Server
- Integrar `run_pipeline` como Prefect Flow

### Fase 4 — API Completa
- Filtros e ordenação nos endpoints
- Paginação melhorada
- Endpoints de repositórios por usuário (`/users/{login}/repositories`)

### Fase 5 — Testes, Docs e Refinamento
- Testes de integração com banco de teste
- Testes E2E
- ADRs em `docs/adr/`
- README completo

---

## Comandos Essenciais

```bash
# Instalar dependências
pip install -e ".[dev]"

# Subir banco
podman-compose -f compose.yaml up -d postgres

# Gerar primeira migration
alembic revision --autogenerate -m "initial"

# Aplicar migrations
alembic upgrade head

# Rodar API local
uvicorn src.main:app --reload

# Rodar testes
pytest

# Pipeline manual
python -c "from src.database.session import SessionLocal; from src.services.pipeline_service import run_pipeline; db = SessionLocal(); print(run_pipeline(db))"
```
