from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database.session import get_db
from src.repositories.user_repository import UserRepository
from src.schemas.schemas import UserResponse, PaginatedResponse

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("", response_model=PaginatedResponse)
def list_users(page: int = 1, page_size: int = 20, db: Session = Depends(get_db)):
    repo = UserRepository(db)
    users, total = repo.get_all(page=page, page_size=page_size)
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
