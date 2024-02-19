# Project settings
import os

from dotenv import load_dotenv


load_dotenv()


def get_url():
    driver = os.getenv("DB_TYPE")
    user = os.getenv("DB_USER")
    password = os.getenv("DB_PASS")
    server = os.getenv("DB_HOST")
    port = os.getenv("DB_PORT")
    db = os.getenv("DB_NAME")
    return f"{driver}://{user}:{password}@{server}:{port}/{db}"


DATABASE_URL = get_url()
