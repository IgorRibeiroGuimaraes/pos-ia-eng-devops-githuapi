from datetime import datetime, timezone

from sqlalchemy import DateTime, Integer, func
from sqlalchemy.orm import Mapped, mapped_column

from src.database.session import Base


class TimestampMixin:
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )


class User(TimestampMixin, Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    github_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    login: Mapped[str] = mapped_column(nullable=False, unique=True, index=True)
    name: Mapped[str | None] = mapped_column(nullable=True)
    followers: Mapped[int] = mapped_column(Integer, default=0)
    following: Mapped[int] = mapped_column(Integer, default=0)
    public_repos: Mapped[int] = mapped_column(Integer, default=0)
    account_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<User(login={self.login!r}, github_id={self.github_id})>"


class Repository(TimestampMixin, Base):
    __tablename__ = "repositories"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    github_repo_id: Mapped[int] = mapped_column(Integer, unique=True, nullable=False, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    language: Mapped[str | None] = mapped_column(nullable=True)
    stars: Mapped[int] = mapped_column(Integer, default=0)
    forks: Mapped[int] = mapped_column(Integer, default=0)
    open_issues: Mapped[int] = mapped_column(Integer, default=0)
    owner_id: Mapped[int] = mapped_column(Integer, nullable=False, index=True)
    repo_created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    repo_updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)

    def __repr__(self) -> str:
        return f"<Repository(name={self.name!r}, github_repo_id={self.github_repo_id})>"


class PipelineExecution(TimestampMixin, Base):
    __tablename__ = "pipeline_executions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    execution_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    pipeline: Mapped[str] = mapped_column(nullable=False)
    status: Mapped[str] = mapped_column(nullable=False)
    records_processed: Mapped[int | None] = mapped_column(Integer, nullable=True)
    execution_time: Mapped[float | None] = mapped_column(nullable=True)
    error_message: Mapped[str | None] = mapped_column(nullable=True)

    def __repr__(self) -> str:
        return f"<PipelineExecution(pipeline={self.pipeline!r}, status={self.status!r})>"
