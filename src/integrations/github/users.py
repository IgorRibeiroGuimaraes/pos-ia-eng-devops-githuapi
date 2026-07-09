from src.integrations.github.client import GitHubClient


def fetch_user(client: GitHubClient, login: str) -> dict:
    return client.get(f"/users/{login}")


def fetch_users_by_query(client: GitHubClient, query: str, per_page: int = 30) -> list[dict]:
    data = client.get("/search/users", params={"q": query, "per_page": per_page})
    logins = [item["login"] for item in data.get("items", [])]
    users = []
    for login in logins:
        try:
            user = fetch_user(client, login)
            users.append(user)
        except Exception:
            continue
    return users
