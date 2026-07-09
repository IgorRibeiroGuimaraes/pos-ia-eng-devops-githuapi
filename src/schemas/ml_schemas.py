from pydantic import BaseModel


class PredictRequest(BaseModel):
    forks: int = 0
    open_issues: int = 0
    followers: int = 0
    public_repos: int = 1
    account_created_at: str  # ISO 8601, ex: "2015-01-01T00:00:00+00:00"


class PredictResponse(BaseModel):
    predicted_stars: int
    features_used: dict


class TrainResponse(BaseModel):
    run_id: str
    r2: float
    mae: float
    rmse: float
    train_samples: int
