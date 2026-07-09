from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.repository_repository import RepositoryRepository
from src.schemas.schemas import RepositoryResponse, PaginatedResponse

router = APIRouter(prefix="/repositories", tags=["Repositories"])


@router.get("", response_model=PaginatedResponse)
def list_repositories(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    repo = RepositoryRepository(db)
    repos, total = repo.get_all(page=page, page_size=page_size)
    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[RepositoryResponse.model_validate(r) for r in repos],
    )


@router.get("/{repo_id}", response_model=RepositoryResponse)
def get_repository(repo_id: int, db: Session = Depends(get_db)):
    repo = RepositoryRepository(db)
    repository = repo.get_by_id(repo_id)
    if not repository:
        raise HTTPException(status_code=404, detail="Repositório não encontrado")
    return RepositoryResponse.model_validate(repository)
