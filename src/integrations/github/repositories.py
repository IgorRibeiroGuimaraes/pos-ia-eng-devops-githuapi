from src.integrations.github.client import GitHubClient


def fetch_user_repositories(client: GitHubClient, login: str, per_page: int = 30) -> list[dict]:
    return client.get(
        f"/users/{login}/repos",
        params={"per_page": per_page, "sort": "updated", "type": "public"},
    )
