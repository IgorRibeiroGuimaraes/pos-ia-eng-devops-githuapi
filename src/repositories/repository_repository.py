from sqlalchemy.orm import Session
from sqlalchemy import text

from src.schemas.schemas import RepositoryCreate


class RepositoryRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def get_by_id(self, repo_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT * FROM repositories WHERE id = :id"),
            {"id": repo_id},
        ).mappings().first()
        return dict(row) if row else None

    def get_by_github_id(self, github_repo_id: int) -> dict | None:
        row = self.db.execute(
            text("SELECT * FROM repositories WHERE github_repo_id = :github_repo_id"),
            {"github_repo_id": github_repo_id},
        ).mappings().first()
        return dict(row) if row else None

    def get_all(self, page: int = 1, page_size: int = 20) -> tuple[list[dict], int]:
        offset = (page - 1) * page_size
        total = self.db.execute(text("SELECT COUNT(*) FROM repositories")).scalar() or 0
        rows = self.db.execute(
            text("SELECT * FROM repositories ORDER BY id LIMIT :limit OFFSET :offset"),
            {"limit": page_size, "offset": offset},
        ).mappings().all()
        return [dict(r) for r in rows], total

    def create(self, data: RepositoryCreate) -> dict:
        row = self.db.execute(
            text("""
                INSERT INTO repositories
                    (github_repo_id, name, language, stars, forks, open_issues,
                     owner_id, repo_created_at, repo_updated_at)
                VALUES
                    (:github_repo_id, :name, :language, :stars, :forks, :open_issues,
                     :owner_id, :repo_created_at, :repo_updated_at)
                RETURNING *
            """),
            data.model_dump(),
        ).mappings().first()
        self.db.commit()
        return dict(row)

    def upsert(self, data: RepositoryCreate) -> dict:
        existing = self.get_by_github_id(data.github_repo_id)
        if existing:
            row = self.db.execute(
                text("""
                    UPDATE repositories
                    SET name            = :name,
                        language        = :language,
                        stars           = :stars,
                        forks           = :forks,
                        open_issues     = :open_issues,
                        owner_id        = :owner_id,
                        repo_created_at = :repo_created_at,
                        repo_updated_at = :repo_updated_at,
                        updated_at      = NOW()
                    WHERE github_repo_id = :github_repo_id
                    RETURNING *
                """),
                data.model_dump(),
            ).mappings().first()
            self.db.commit()
            return dict(row)
        return self.create(data)

    def get_statistics(self) -> dict:
        stats = self.db.execute(
            text("""
                SELECT
                    COUNT(*)                        AS total_repositories,
                    COALESCE(SUM(stars), 0)         AS total_stars,
                    COALESCE(AVG(stars), 0)         AS average_stars
                FROM repositories
            """)
        ).mappings().first()

        lang_row = self.db.execute(
            text("""
                SELECT language
                FROM repositories
                WHERE language IS NOT NULL
                GROUP BY language
                ORDER BY COUNT(*) DESC
                LIMIT 1
            """)
        ).first()

        return {
            "total_repositories": stats["total_repositories"],
            "total_stars": int(stats["total_stars"]),
            "average_stars": round(float(stats["average_stars"]), 2),
            "most_used_language": lang_row[0] if lang_row else None,
        }
