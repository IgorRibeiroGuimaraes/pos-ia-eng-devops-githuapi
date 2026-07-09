import pytest
from src.jobs.transform import transform_user, transform_repository, enrich_user


RAW_USER = {
    "id": 1,
    "login": "octocat",
    "name": "The Octocat",
    "followers": 10000,
    "following": 9,
    "public_repos": 8,
    "created_at": "2011-01-25T18:44:36Z",
}

RAW_REPO = {
    "id": 1296269,
    "name": "Hello-World",
    "language": "Python",
    "stargazers_count": 100,
    "forks_count": 50,
    "open_issues_count": 3,
    "created_at": "2011-01-26T19:01:12Z",
    "updated_at": "2023-01-01T00:00:00Z",
}


def test_transform_user():
    result = transform_user(RAW_USER)
    assert result.login == "octocat"
    assert result.github_id == 1
    assert result.followers == 10000


def test_transform_repository():
    result = transform_repository(RAW_REPO, owner_id=42)
    assert result.name == "Hello-World"
    assert result.github_repo_id == 1296269
    assert result.owner_id == 42
    assert result.language == "Python"


def test_enrich_user():
    result = enrich_user(RAW_USER)
    assert "_enriched" in result
    assert result["_enriched"]["followers_per_repo"] > 0
    assert result["_enriched"]["account_age_years"] > 0
