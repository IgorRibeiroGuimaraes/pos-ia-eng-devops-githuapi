from sqlalchemy.orm import Session
from sqlalchemy import text

from src.schemas.schemas import UserCreate


class UserRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_login(self, login: str) -> dict | None:
        row = self.db.execute(
            text("SELECT * FROM users WHERE login = :login"),
            {"login": login},
        ).mappings().first()
        return dict(row) if row else None

    def get_by_github_id(self, github_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT * FROM users WHERE github_id = :github_id"),
            {"github_id": github_id},
        ).mappings().first()
        return dict(row) if row else None

    def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        offset = (page - 1) * page_size
        total = self.db.execute(text("SELECT COUNT(*) FROM users")).scalar() or 0
        rows = self.db.execute(
            text("SELECT * FROM users ORDER BY id LIMIT :limit OFFSET :offset"),
            {"limit": page_size, "offset": offset},
        ).mappings().all()
        return [dict(r) for r in rows], total

    def create(self, data: UserCreate) -> dict:
        row = self.db.execute(
            text("""
                INSERT INTO users
                    (github_id, login, name, followers, following, public_repos, account_created_at)
                VALUES
                    (:github_id, :login, :name, :followers, :following, :public_repos, :account_created_at)
                RETURNING *
            """),
            data.model_dump(),
        ).mappings().first()
        self.db.commit()
        return dict(row)

    def upsert(self, data: UserCreate) -> dict:
        existing = self.get_by_github_id(data.github_id)
        if existing:
            row = self.db.execute(
                text("""
                    UPDATE users
                    SET login               = :login,
                        name                = :name,
                        followers           = :followers,
                        following           = :following,
                        public_repos        = :public_repos,
                        account_created_at  = :account_created_at,
                        updated_at          = NOW()
                    WHERE github_id = :github_id
                    RETURNING *
                """),
                data.model_dump(),
            ).mappings().first()
            self.db.commit()
            return dict(row)
        return self.create(data)
