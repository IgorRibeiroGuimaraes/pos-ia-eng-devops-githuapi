from fastapi import APIRouter, BackgroundTasks, Depends
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.pipeline_repository import PipelineExecutionRepository
from src.schemas.schemas import PipelineExecutionResponse
from src.services.pipeline_service import run_pipeline

router = APIRouter(prefix="/admin", tags=["Admin"])


@router.post("/run-pipeline")
def trigger_pipeline(
    background_tasks: BackgroundTasks,
    query: str = "language:python followers:>100",
    db: Session = Depends(get_db),
):
    background_tasks.add_task(run_pipeline, db, query)
    return {"message": "Pipeline iniciado em background", "query": query}


@router.get("/status", response_model=PipelineExecutionResponse | None)
def pipeline_status(pipeline: str = "github_pipeline", db: Session = Depends(get_db)):
    repo = PipelineExecutionRepository(db)
    execution = repo.get_latest(pipeline=pipeline)
    if not execution:
        return None
    return PipelineExecutionResponse.model_validate(execution)
