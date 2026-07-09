from datetime import datetime

from pydantic import BaseModel, Field


# ── User Schemas ──────────────────────────────────────────────────────────────

class UserBase(BaseModel):
    login: str
    name: str | None = None
    followers: int = 0
    following: int = 0
    public_repos: int = 0
    account_created_at: datetime


class UserCreate(UserBase):
    github_id: int


class UserResponse(UserBase):
    id: int
    github_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Repository Schemas ────────────────────────────────────────────────────────

class RepositoryBase(BaseModel):
    name: str
    language: str | None = None
    stars: int = 0
    forks: int = 0
    open_issues: int = 0
    repo_created_at: datetime
    repo_updated_at: datetime


class RepositoryCreate(RepositoryBase):
    github_repo_id: int
    owner_id: int


class RepositoryResponse(RepositoryBase):
    id: int
    github_repo_id: int
    owner_id: int
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


# ── Pagination ────────────────────────────────────────────────────────────────

class PaginatedResponse(BaseModel):
    total: int
    page: int
    page_size: int
    items: list


# ── Pipeline Schemas ──────────────────────────────────────────────────────────

class PipelineExecutionResponse(BaseModel):
    id: int
    execution_date: datetime
    pipeline: str
    status: str
    records_processed: int | None = None
    execution_time: float | None = None
    error_message: str | None = None
    created_at: datetime

    model_config = {"from_attributes": True}


# ── Statistics ────────────────────────────────────────────────────────────────

class StatisticsResponse(BaseModel):
    total_users: int
    total_repositories: int
    most_used_language: str | None = None
    average_stars: float = 0.0
    total_stars: int = 0
