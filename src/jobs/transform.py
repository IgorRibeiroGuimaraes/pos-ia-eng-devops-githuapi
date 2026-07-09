from datetime import UTC, datetime

from src.schemas.schemas import RepositoryCreate, UserCreate


def transform_user(raw: dict) -> UserCreate:
    return UserCreate(
        github_id=raw["id"],
        login=raw["login"],
        name=raw.get("name"),
        followers=raw.get("followers", 0),
        following=raw.get("following", 0),
        public_repos=raw.get("public_repos", 0),
        account_created_at=datetime.fromisoformat(raw["created_at"].replace("Z", "+00:00")),
    )


def transform_repository(raw: dict, owner_id: int) -> RepositoryCreate:
    return RepositoryCreate(
        github_repo_id=raw["id"],
        name=raw["name"],
        language=raw.get("language"),
        stars=raw.get("stargazers_count", 0),
        forks=raw.get("forks_count", 0),
        open_issues=raw.get("open_issues_count", 0),
        owner_id=owner_id,
        repo_created_at=datetime.fromisoformat(raw["created_at"].replace("Z", "+00:00")),
        repo_updated_at=datetime.fromisoformat(raw["updated_at"].replace("Z", "+00:00")),
    )


def enrich_user(raw: dict) -> dict:
    """Adiciona métricas derivadas ao usuário."""
    followers = raw.get("followers", 0)
    public_repos = raw.get("public_repos", 1) or 1
    created_at = raw.get("created_at", "")

    account_age_years = 0
    if created_at:
        created = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
        account_age_years = max(
            (datetime.now(UTC) - created).days / 365.25, 0.01
        )

    return {
        **raw,
        "_enriched": {
            "followers_per_repo": round(followers / public_repos, 2),
            "repos_per_year": round(public_repos / account_age_years, 2),
            "account_age_years": round(account_age_years, 2),
        },
    }
