# Project settings
import os

from dotenv import load_dotenv


load_dotenv()


class Config:
    DATABASE_URL = os.environ.get(
        "DATABASE_URL", "postgresql://user:password@localhost:port/dbname"
    )


settings = Config()
