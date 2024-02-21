# Project settings
import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@localhost:port/dbname"
    )
    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

    CELERY_BROKER_URL = os.environ.get("CELERY_BROKER_URL", "redis://127.0.0.1:6379/0")
    CELERY_RESULT_BACKEND = os.environ.get(
        "CELERY_RESULT_BACKEND", "redis://127.0.0.1:6379/0"
    )


settings = Config()
