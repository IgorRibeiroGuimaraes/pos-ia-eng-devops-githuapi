from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.user_repository import UserRepository
from src.repositories.repository_repository import RepositoryRepository
from src.schemas.schemas import UserResponse, RepositoryResponse, PaginatedResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse)
def list_users(
    page: int = 1,
    page_size: int = 20,
    order_by: str = "id",
    order_dir: str = "asc",
    min_followers: int | None = None,
    db: Session = Depends(get_db),
):
    repo = UserRepository(db)
    users, total = repo.get_all(
        page=page,
        page_size=page_size,
        order_by=order_by,
        order_dir=order_dir,
        min_followers=min_followers,
    )
    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[UserResponse.model_validate(u) for u in users],
    )


@router.get("/{login}", response_model=UserResponse)
def get_user(login: str, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    user = repo.get_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    return UserResponse.model_validate(user)


@router.get("/{login}/repositories", response_model=PaginatedResponse)
def list_user_repositories(
    login: str,
    page: int = 1,
    page_size: int = 20,
    db: Session = Depends(get_db),
):
    user = UserRepository(db).get_by_login(login)
    if not user:
        raise HTTPException(status_code=404, detail="Usuário não encontrado")
    repos, total = RepositoryRepository(db).get_by_owner_id(
        owner_id=user["id"],
        page=page,
        page_size=page_size,
    )
    return PaginatedResponse(
        total=total,
        page=page,
        page_size=page_size,
        items=[RepositoryResponse.model_validate(r) for r in repos],
    )
