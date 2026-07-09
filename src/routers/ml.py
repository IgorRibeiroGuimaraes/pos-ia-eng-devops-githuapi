from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.ml.predict import predict_stars
from src.ml.train import train
from src.schemas.ml_schemas import PredictRequest, PredictResponse, TrainResponse

router = APIRouter(prefix="/ml", tags=["MLOps"])


@router.post("/train", response_model=TrainResponse)
def trigger_training(db: Session = Depends(get_db)):
    """
    Treina o modelo de popularidade usando os dados do banco.
    Rastreia métricas e versiona o modelo no MLflow.
    """
    try:
        result = train(db)
        return TrainResponse(**result)
    except ValueError as exc:
        raise HTTPException(status_code=422, detail=str(exc))
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro no treino: {exc}")


@router.post("/predict", response_model=PredictResponse)
def predict(body: PredictRequest):
    """
    Prediz a quantidade de estrelas esperadas para um repositório
    com base nas características fornecidas.
    """
    try:
        repo_data = {
            "forks": body.forks,
            "open_issues": body.open_issues,
            "stars": 0,
        }
        user_data = {
            "followers": body.followers,
            "public_repos": body.public_repos,
            "account_created_at": body.account_created_at,
        }
        result = predict_stars(repo_data, user_data)
        return PredictResponse(**result)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=f"Erro na predição: {exc}")
