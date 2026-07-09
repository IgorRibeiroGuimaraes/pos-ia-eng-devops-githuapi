"""
Inferência: carrega o modelo registrado no MLflow e retorna predições.
"""

import mlflow.sklearn
import pandas as pd

from src.core.config import settings
from src.core.logging import get_logger
from src.ml.features import FEATURE_COLUMNS, build_features
from src.ml.train import MODEL_NAME

logger = get_logger(__name__)

_model_cache: object = None


def _load_model():
    global _model_cache
    if _model_cache is None:
        mlflow.set_tracking_uri(settings.mlflow_tracking_uri)
        _model_cache = mlflow.sklearn.load_model(f"models:/{MODEL_NAME}/latest")
        logger.info(f"Modelo '{MODEL_NAME}' carregado do MLflow")
    return _model_cache


def predict_stars(repo_data: dict, user_data: dict) -> dict:
    """
    Prediz a quantidade de estrelas esperadas para um repositório.

    Args:
        repo_data: dict com chaves forks, open_issues, stars (pode ser 0)
        user_data: dict com chaves followers, public_repos, account_created_at

    Returns:
        dict com predicted_stars e features usadas
    """
    import mlflow
    mlflow.set_tracking_uri(settings.mlflow_tracking_uri)

    row = {**repo_data, **user_data}
    df = build_features([row])
    features = df[FEATURE_COLUMNS]

    model = _load_model()
    prediction = float(model.predict(features)[0])

    return {
        "predicted_stars": max(0, round(prediction)),
        "features_used": features.iloc[0].to_dict(),
    }
