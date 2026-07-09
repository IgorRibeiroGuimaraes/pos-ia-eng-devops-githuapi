"""
Treino do modelo de popularidade com rastreamento via MLflow.

Fluxo:
  1. Carrega dados do PostgreSQL (JOIN repositories + users)
  2. Engenharia de features
  3. Split treino/teste
  4. Treina GradientBoostingRegressor
  5. Loga métricas, parâmetros e modelo no MLflow
  6. Registra modelo no MLflow Model Registry
"""

import mlflow
import mlflow.sklearn
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.core.config import settings
from src.core.logging import get_logger
from src.ml.features import FEATURE_COLUMNS, TARGET_COLUMN, build_features

logger = get_logger(__name__)

MODEL_NAME = "github-repo-popularity"


def _load_training_data(db: Session) -> list[dict]:
    rows = db.execute(
        text("""
            SELECT
                r.stars,
                r.forks,
                r.open_issues,
                u.followers,
                u.public_repos,
                u.account_created_at
            FROM repositories r
            JOIN users u ON r.owner_id = u.id
        """)
    ).mappings().all()
    return [dict(row) for row in rows]


def train(db: Session) -> dict:
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
    mlflow.set_experiment(settings.mlflow_experiment_name)

    rows = _load_training_data(db)
    if len(rows) < 10:
        raise ValueError(f"Dados insuficientes para treino: {len(rows)} registros (mínimo 10)")

    df = build_features(rows)
    x_feat = df[FEATURE_COLUMNS]
    y = df[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        x_feat, y, test_size=0.2, random_state=42
    )

    params = {
        "n_estimators": 100,
        "max_depth": 4,
        "learning_rate": 0.1,
        "random_state": 42,
    }

    pipeline = Pipeline(
        [
            ("scaler", StandardScaler()),
            ("model", GradientBoostingRegressor(**params)),
        ]
    )

    with mlflow.start_run() as run:
        pipeline.fit(x_train, y_train)
        y_pred = pipeline.predict(x_test)

        metrics = {
            "mae": float(mean_absolute_error(y_test, y_pred)),
            "rmse": float(np.sqrt(mean_squared_error(y_test, y_pred))),
            "r2": float(r2_score(y_test, y_pred)),
        }

        mlflow.log_params(params)
        mlflow.log_metrics(metrics)
        mlflow.log_param("train_samples", len(x_train))
        mlflow.log_param("test_samples", len(x_test))
        mlflow.log_param("features", FEATURE_COLUMNS)

        mlflow.sklearn.log_model(
            pipeline,
            artifact_path="model",
            registered_model_name=MODEL_NAME,
            input_example=x_test.head(3),
        )

        run_id = run.info.run_id
        logger.info(f"Treino concluído — run_id={run_id} | R²={metrics['r2']:.3f} | MAE={metrics['mae']:.1f}")

    return {"run_id": run_id, **metrics, "train_samples": len(x_train)}
