from datetime import UTC, datetime

from sqlalchemy import text


def _insert_user(db, *, login: str = "octocat", github_id: int = 1) -> dict:
    row = db.execute(
        text("""
            INSERT INTO users (github_id, login, name, followers, following, public_repos, account_created_at)
            VALUES (:github_id, :login, :name, :followers, :following, :public_repos, :account_created_at)
            RETURNING *
        """),
        {
            "github_id": github_id,
            "login": login,
            "name": "Test User",
            "followers": 500,
            "following": 10,
            "public_repos": 20,
            "account_created_at": datetime(2015, 1, 1, tzinfo=UTC),
        },
    ).mappings().first()
    db.commit()
    return dict(row)


def _insert_repository(db, *, owner_id: int, name: str = "hello-world", github_repo_id: int = 100) -> dict:
    row = db.execute(
        text("""
            INSERT INTO repositories
                (github_repo_id, name, language, stars, forks, open_issues, owner_id, repo_created_at, repo_updated_at)
            VALUES
                (:github_repo_id, :name, :language, :stars, :forks, :open_issues, :owner_id, :repo_created_at, :repo_updated_at)
            RETURNING *
        """),
        {
            "github_repo_id": github_repo_id,
            "name": name,
            "language": "Python",
            "stars": 42,
            "forks": 5,
            "open_issues": 2,
            "owner_id": owner_id,
            "repo_created_at": datetime(2020, 1, 1, tzinfo=UTC),
            "repo_updated_at": datetime(2024, 1, 1, tzinfo=UTC),
        },
    ).mappings().first()
    db.commit()
    return dict(row)


def test_get_user_by_login(client, db):
    _insert_user(db, login="octocat", github_id=9999)
    r = client.get("/users/octocat")
    assert r.status_code == 200
    data = r.json()
    assert data["login"] == "octocat"
    assert data["followers"] == 500


def test_list_users_with_data(client, db):
    _insert_user(db, login="userA", github_id=1001)
    _insert_user(db, login="userB", github_id=1002)
    r = client.get("/users")
    assert r.status_code == 200
    assert r.json()["total"] >= 2


def test_user_repositories(client, db):
    user = _insert_user(db, login="repoowner", github_id=2001)
    _insert_repository(db, owner_id=user["id"], name="repo1", github_repo_id=3001)
    _insert_repository(db, owner_id=user["id"], name="repo2", github_repo_id=3002)

    r = client.get("/users/repoowner/repositories")
    assert r.status_code == 200
    data = r.json()
    assert data["total"] == 2
    assert len(data["items"]) == 2


def test_statistics_with_data(client, db):
    user = _insert_user(db, login="statsuser", github_id=5001)
    _insert_repository(db, owner_id=user["id"], github_repo_id=6001)

    r = client.get("/statistics")
    assert r.status_code == 200
    data = r.json()
    assert data["total_users"] >= 1
    assert data["total_repositories"] >= 1
    assert data["most_used_language"] == "Python"


def test_repositories_filter_language(client, db):
    user = _insert_user(db, login="filteruser", github_id=7001)
    _insert_repository(db, owner_id=user["id"], name="py-repo", github_repo_id=8001)

    r = client.get("/repositories?language=Python")
    assert r.status_code == 200
    items = r.json()["items"]
    assert all(i["language"] == "Python" for i in items)


def test_repositories_filter_min_stars(client, db):
    user = _insert_user(db, login="staruser", github_id=9001)
    _insert_repository(db, owner_id=user["id"], name="popular", github_repo_id=10001)

    r = client.get("/repositories?min_stars=10")
    assert r.status_code == 200
    items = r.json()["items"]
    assert all(i["stars"] >= 10 for i in items)
