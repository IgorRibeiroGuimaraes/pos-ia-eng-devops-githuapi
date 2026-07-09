from datetime import UTC, datetime

from sqlalchemy.orm import Session

from src.core.logging import get_logger
from src.integrations.github.client import GitHubClient
from src.integrations.github.repositories import fetch_user_repositories
from src.integrations.github.users import fetch_users_by_query
from src.jobs.transform import enrich_user, transform_repository, transform_user
from src.repositories.pipeline_repository import PipelineExecutionRepository
from src.repositories.repository_repository import RepositoryRepository
from src.repositories.user_repository import UserRepository

logger = get_logger(__name__)


def run_pipeline(db: Session, query: str = "language:python followers:>100") -> dict:
    exec_repo = PipelineExecutionRepository(db)
    start = datetime.now(UTC)
    execution = exec_repo.create(
        {
            "execution_date": start,
            "pipeline": "github_pipeline",
            "status": "running",
        }
    )

    users_processed = 0
    repos_processed = 0

    try:
        user_repo = UserRepository(db)
        repo_repo = RepositoryRepository(db)

        with GitHubClient() as client:
            # Extract & Transform users
            logger.info("Extraindo usuários da GitHub API...")
            raw_users = fetch_users_by_query(client, query)

            for raw_user in raw_users:
                enriched = enrich_user(raw_user)
                user_data = transform_user(enriched)
                db_user = user_repo.upsert(user_data)
                users_processed += 1

                # Extract & Transform repositories
                raw_repos = fetch_user_repositories(client, db_user["login"])
                for raw_repo in raw_repos:
                    repo_data = transform_repository(raw_repo, db_user["id"])
                    repo_repo.upsert(repo_data)
                    repos_processed += 1

        elapsed = (datetime.now(UTC) - start).total_seconds()
        total_records = users_processed + repos_processed

        exec_repo.update(
            execution["id"],
            {
                "status": "success",
                "records_processed": total_records,
                "execution_time": elapsed,
            },
        )

        logger.info(f"Pipeline concluído: {users_processed} usuários, {repos_processed} repos")
        return {
            "status": "success",
            "users_processed": users_processed,
            "repos_processed": repos_processed,
            "execution_time": elapsed,
        }

    except Exception as exc:
        elapsed = (datetime.now(UTC) - start).total_seconds()
        exec_repo.update(
            execution["id"],
            {
                "status": "error",
                "execution_time": elapsed,
                "error_message": str(exc),
            },
        )
        logger.error(f"Erro no pipeline: {exc}")
        raise
