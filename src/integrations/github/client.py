import httpx

from src.core.config import settings
from src.core.logging import get_logger

logger = get_logger(__name__)


class GitHubClient:
    def __init__(self) -> None:
        headers = {
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
        }
        if settings.github_token:
            headers["Authorization"] = f"Bearer {settings.github_token}"

        self._client = httpx.Client(
            base_url=settings.github_api_base_url,
            headers=headers,
            timeout=30.0,
        )

    def get(self, path: str, params: dict | None = None) -> dict:
        logger.info(f"GitHub API GET {path}")
        response = self._client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    def close(self) -> None:
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()
