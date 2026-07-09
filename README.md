# GitHub Data Pipeline API

Pipeline de Engenharia de Dados que consome a GitHub API, processa e enriquece os dados via ETL orquestrado com Prefect, persiste em PostgreSQL e os disponibiliza através de uma API REST construída com FastAPI.

---

## Stack

| Tecnologia | Finalidade |
|---|---|
| Python 3.12 | Linguagem principal |
| FastAPI | API REST |
| PostgreSQL 16 | Banco de Dados |
| SQLAlchemy 2.x | ORM (apenas para Alembic) |
| Alembic | Migrações |
| Prefect 3 | Orquestração ETL |
| Podman | Containers |
| GitHub Actions | CI/CD |
| HTTPX | Cliente HTTP |
| Pydantic v2 | Validação e serialização |
| Pytest | Testes |
| Ruff + Black | Linter e formatação |

---

## Arquitetura

```
GitHub API → Prefect Flow (Extract → Validate → Transform → Enrich → Load) → PostgreSQL → FastAPI REST
```

### Camadas

```
Routers → Services → Repositories (SQL raw) → PostgreSQL
```

---

## Início Rápido

### Pré-requisitos

- Python 3.12+
- Podman + podman-compose
- Git

### Setup

```bash
# 1. Clonar e entrar no projeto
git clone <repo-url>
cd pos-ia-devops

# 2. Criar ambiente virtual e instalar dependências
python -m venv .venv
.venv\Scripts\activate        # Windows
pip install -e ".[dev]"

# 3. Copiar variáveis de ambiente
cp .env.example .env
# Edite .env e adicione seu GITHUB_TOKEN (opcional, mas recomendado)

# 4. Subir o banco
podman-compose -f compose.yaml up -d postgres

# 5. Aplicar migrations
alembic upgrade head

# 6. Rodar a API
uvicorn src.main:app --reload
```

Acesse `http://localhost:8000/docs` para a documentação interativa.

---

## Endpoints

### Públicos

| Método | Endpoint | Descrição |
|---|---|---|
| GET | `/health` | Status da API |
| GET | `/users` | Listar usuários (filtros: `min_followers`, `order_by`, `order_dir`) |
| GET | `/users/{login}` | Buscar usuário por login |
| GET | `/users/{login}/repositories` | Repositórios de um usuário |
| GET | `/repositories` | Listar repositórios (filtros: `language`, `min_stars`, `order_by`, `order_dir`) |
| GET | `/repositories/{id}` | Buscar repositório por ID |
| GET | `/statistics` | Estatísticas gerais |

### Administrativos

| Método | Endpoint | Descrição |
|---|---|---|
| POST | `/admin/run-pipeline` | Executar pipeline em background |
| GET | `/admin/status` | Status da última execução |

---

## Pipeline ETL

```
extract_users → enrich_user → transform_user → load_user
                                    ↓
             extract_repositories → transform_repository → load_repository
```

### Executar manualmente

```bash
# Via script Python
python -m src.prefect.flows

# Via endpoint da API
curl -X POST "http://localhost:8000/admin/run-pipeline?query=language:python+followers:>100"
```

---

## Enriquecimento de Dados

Além dos dados da API, o pipeline calcula métricas derivadas:

- `followers_per_repo` — Seguidores por repositório
- `repos_per_year` — Repositórios criados por ano
- `account_age_years` — Idade da conta em anos

---

## Testes

```bash
# Unitários
pytest tests/unit -v

# Integração (requer PostgreSQL rodando)
pytest tests/integration -v

# Todos com cobertura
pytest --cov=src --cov-report=html
```

---

## Makefile

```bash
make up          # Subir todos os containers
make down        # Parar containers
make migrate     # Aplicar migrations
make revision msg="descrição"  # Gerar nova migration
make test        # Rodar testes
make lint        # Verificar código
make format      # Formatar código
make run-pipeline  # Executar pipeline manualmente
```

---

## Containers

```bash
# Subir tudo
podman-compose -f compose.yaml up -d

# Serviços disponíveis:
# API:            http://localhost:8000
# Docs:           http://localhost:8000/docs
# pgAdmin:        http://localhost:5050
# Prefect UI:     http://localhost:4200
```

---

## Decisões Arquiteturais

Ver [`docs/adr/`](docs/adr/) para os registros de decisão.

---

## CI/CD

O GitHub Actions executa automaticamente em push para `main` e `develop`:

1. **Lint** — Ruff + Black
2. **Tests** — Pytest com PostgreSQL de serviço
3. **Build** — Imagem Podman
