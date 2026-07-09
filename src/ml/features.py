"""
Feature engineering para o modelo de popularidade de repositórios.

Problema: regressão para prever quantidade de estrelas de um repositório
com base em características do repositório e do dono.

Features:
  - forks            : correlacionado com popularidade
  - open_issues      : indicador de atividade
  - followers        : popularidade do dono
  - public_repos     : tamanho do portfólio do dono
  - account_age_days : maturidade do dono
  - repos_per_year   : produtividade do dono

Target:
  - stars
"""

from datetime import UTC, datetime

import pandas as pd

FEATURE_COLUMNS = [
    "forks",
    "open_issues",
    "followers",
    "public_repos",
    "account_age_days",
    "repos_per_year",
]

TARGET_COLUMN = "stars"


def build_features(rows: list[dict]) -> pd.DataFrame:
    """
    Recebe lista de dicts com JOIN de repositories + users
    e retorna DataFrame com features + target prontos para treino.
    """
    records = []
    for row in rows:
        account_created_at = row.get("account_created_at")
        if isinstance(account_created_at, str):
            account_created_at = datetime.fromisoformat(account_created_at)
        if account_created_at and account_created_at.tzinfo is None:
            account_created_at = account_created_at.replace(tzinfo=UTC)

        age_days = (
            (datetime.now(UTC) - account_created_at).days
            if account_created_at
            else 0
        )
        age_years = max(age_days / 365.25, 0.01)

        records.append(
            {
                "forks": int(row.get("forks", 0)),
                "open_issues": int(row.get("open_issues", 0)),
                "followers": int(row.get("followers", 0)),
                "public_repos": int(row.get("public_repos", 1)),
                "account_age_days": age_days,
                "repos_per_year": round(int(row.get("public_repos", 1)) / age_years, 2),
                TARGET_COLUMN: int(row.get("stars", 0)),
            }
        )

    return pd.DataFrame(records)
