from fastapi import APIRouter, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.repository_repository import RepositoryRepository
from src.schemas.schemas import StatisticsResponse

router = APIRouter(prefix="/statistics", tags=["Statistics"])


@router.get("", response_model=StatisticsResponse)
def get_statistics(db: Session = Depends(get_db)):
    total_users = db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
    repo_stats = RepositoryRepository(db).get_statistics()

    return StatisticsResponse(
        total_users=total_users,
        total_repositories=repo_stats["total_repositories"],
        most_used_language=repo_stats["most_used_language"],
        average_stars=repo_stats["average_stars"],
        total_stars=repo_stats["total_stars"],
    )
