from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from src.core.config import settings
from src.routers import users, repositories, statistics, admin

app = FastAPI(
    title="GitHub Data Pipeline API",
    description="Pipeline de Engenharia de Dados com GitHub API, FastAPI e Prefect",
    version="0.1.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(users.router)
app.include_router(repositories.router)
app.include_router(statistics.router)
app.include_router(admin.router)


@app.get("/health", tags=["Health"])
def health_check():
    return {"status": "ok", "environment": settings.environment}
