from sqlalchemy import text
from sqlalchemy.orm import Session

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

    def get_all(
        self,
        page: int = 1,
        page_size: int = 20,
        order_by: str = "id",
        order_dir: str = "asc",
        min_followers: int | None = None,
    ) -> tuple[list[dict], int]:
        _allowed_order = {"id", "login", "followers", "public_repos", "account_created_at"}
        _allowed_dir = {"asc", "desc"}
        if order_by not in _allowed_order:
            order_by = "id"
        if order_dir not in _allowed_dir:
            order_dir = "asc"

        offset = (page - 1) * page_size
        where = "WHERE followers >= :min_followers" if min_followers is not None else ""
        params: dict = {"limit": page_size, "offset": offset}
        if min_followers is not None:
            params["min_followers"] = min_followers

        total = self.db.execute(
            text(f"SELECT COUNT(*) FROM users {where}"),
            params,
        ).scalar() or 0
        rows = self.db.execute(
            text(f"SELECT * FROM users {where} ORDER BY {order_by} {order_dir} LIMIT :limit OFFSET :offset"),
            params,
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
