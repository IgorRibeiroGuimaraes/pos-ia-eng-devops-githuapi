from sqlalchemy import text
from sqlalchemy.orm import Session

# Colunas permitidas no UPDATE — impede injeção via nomes de campo dinâmicos
_UPDATABLE_FIELDS = frozenset({"status", "records_processed", "execution_time", "error_message"})


class PipelineExecutionRepository:
    def __init__(self, db: Session) -> None:
        self.db = db

    def create(self, data: dict) -> dict:
        row = (
            self.db.execute(
                text("""
                INSERT INTO pipeline_executions
                    (execution_date, pipeline, status, records_processed, execution_time, error_message)
                VALUES
                    (:execution_date, :pipeline, :status,
                     :records_processed, :execution_time, :error_message)
                RETURNING *
            """),
                {
                    "execution_date": data["execution_date"],
                    "pipeline": data["pipeline"],
                    "status": data["status"],
                    "records_processed": data.get("records_processed"),
                    "execution_time": data.get("execution_time"),
                    "error_message": data.get("error_message"),
                },
            )
            .mappings()
            .first()
        )
        self.db.commit()
        return dict(row)

    def update(self, execution_id: int, data: dict) -> dict | None:
        invalid = set(data.keys()) - _UPDATABLE_FIELDS
        if invalid:
            raise ValueError(f"Campos não permitidos para atualização: {invalid}")

        row = (
            self.db.execute(
                text("""
                UPDATE pipeline_executions
                SET
                    status             = COALESCE(:status,             status),
                    records_processed  = COALESCE(:records_processed,  records_processed),
                    execution_time     = COALESCE(:execution_time,      execution_time),
                    error_message      = COALESCE(:error_message,       error_message)
                WHERE id = :_id
                RETURNING *
            """),
                {
                    "status": data.get("status"),
                    "records_processed": data.get("records_processed"),
                    "execution_time": data.get("execution_time"),
                    "error_message": data.get("error_message"),
                    "_id": execution_id,
                },
            )
            .mappings()
            .first()
        )
        self.db.commit()
        return dict(row) if row else None

    def get_latest(self, pipeline: str | None = None) -> dict | None:
        if pipeline:
            row = (
                self.db.execute(
                    text("""
                    SELECT * FROM pipeline_executions
                    WHERE pipeline = :pipeline
                    ORDER BY execution_date DESC
                    LIMIT 1
                """),
                    {"pipeline": pipeline},
                )
                .mappings()
                .first()
            )
        else:
            row = self.db.execute(text("""
                    SELECT * FROM pipeline_executions
                    ORDER BY execution_date DESC
                    LIMIT 1
                """)).mappings().first()
        return dict(row) if row else None
