from prefect import flow, get_run_logger, task
from src.database.session import SessionLocal
from src.ml.train import train


@task(name="train-popularity-model")
def task_train_model() -> dict:
    logger = get_run_logger()
    db = SessionLocal()
    try:
        logger.info("Iniciando treino do modelo de popularidade...")
        result = train(db)
        logger.info(
            f"Modelo treinado | R²={result['r2']:.3f} | MAE={result['mae']:.1f} | "
            f"run_id={result['run_id']}"
        )
        return result
    finally:
        db.close()


@flow(name="ml-training-pipeline", log_prints=True)
def ml_training_pipeline() -> dict:
    """
    Flow Prefect para treino do modelo de popularidade de repositórios.
    Deve ser executado após o pipeline ETL ter populado o banco.
    """
    logger = get_run_logger()
    logger.info("Iniciando pipeline de treino MLOps")
    result = task_train_model()
    logger.info(f"Pipeline de treino concluído: {result}")
    return result


if __name__ == "__main__":
    ml_training_pipeline()
