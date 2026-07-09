from datetime import UTC, datetime

from prefect import flow, get_run_logger, task
from src.database.session import SessionLocal
from src.integrations.github.client import GitHubClient
from src.integrations.github.repositories import fetch_user_repositories
from src.integrations.github.users import fetch_users_by_query
from src.jobs.transform import enrich_user, transform_repository, transform_user
from src.repositories.pipeline_repository import PipelineExecutionRepository
from src.repositories.repository_repository import RepositoryRepository
from src.repositories.user_repository import UserRepository


@task(name="extract-users", retries=3, retry_delay_seconds=10)
def task_extract_users(query: str) -> list[dict]:
    logger = get_run_logger()
    logger.info(f"Extraindo usuários com query: {query}")
    with GitHubClient() as client:
        raw_users = fetch_users_by_query(client, query)
    logger.info(f"{len(raw_users)} usuários extraídos")
    return raw_users


@task(name="extract-repositories", retries=3, retry_delay_seconds=10)
def task_extract_repositories(login: str) -> list[dict]:
    logger = get_run_logger()
    logger.info(f"Extraindo repositórios de: {login}")
    with GitHubClient() as client:
        return fetch_user_repositories(client, login)


@task(name="enrich-user")
def task_enrich_user(raw_user: dict) -> dict:
    return enrich_user(raw_user)


@task(name="transform-user")
def task_transform_user(enriched: dict):
    return transform_user(enriched)


@task(name="transform-repository")
def task_transform_repository(raw_repo: dict, owner_id: int):
    return transform_repository(raw_repo, owner_id)


@task(name="load-user")
def task_load_user(user_data) -> dict:
    db = SessionLocal()
    try:
        return UserRepository(db).upsert(user_data)
    finally:
        db.close()


@task(name="load-repository")
def task_load_repository(repo_data) -> dict:
    db = SessionLocal()
    try:
        return RepositoryRepository(db).upsert(repo_data)
    finally:
        db.close()


@flow(name="github-pipeline", log_prints=True)
def github_pipeline(query: str = "language:python followers:>100") -> dict:
    logger = get_run_logger()
    db = SessionLocal()
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
        raw_users = task_extract_users(query)

        for raw_user in raw_users:
            enriched = task_enrich_user(raw_user)
            user_data = task_transform_user(enriched)
            db_user = task_load_user(user_data)
            users_processed += 1

            raw_repos = task_extract_repositories(db_user["login"])
            for raw_repo in raw_repos:
                repo_data = task_transform_repository(raw_repo, db_user["id"])
                task_load_repository(repo_data)
                repos_processed += 1

        elapsed = (datetime.now(UTC) - start).total_seconds()
        exec_repo.update(
            execution["id"],
            {
                "status": "success",
                "records_processed": users_processed + repos_processed,
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
    finally:
        db.close()


if __name__ == "__main__":
    github_pipeline()
