import os
from urllib.parse import quote_plus

from dotenv import load_dotenv

load_dotenv()


def _build_database_uri():
    database_url = os.getenv("DATABASE_URL") or os.getenv("MYSQL_URL")
    if database_url:
        if database_url.startswith("mysql://"):
            return database_url.replace("mysql://", "mysql+pymysql://", 1)
        return database_url

    user = os.getenv("DB_USER") or os.getenv("MYSQLUSER", "root")
    password = os.getenv("DB_PASSWORD") or os.getenv("MYSQLPASSWORD", "root123")
    host = os.getenv("DB_HOST") or os.getenv("MYSQLHOST", "localhost")
    port = os.getenv("DB_PORT") or os.getenv("MYSQLPORT", "3306")
    name = os.getenv("DB_NAME") or os.getenv("MYSQLDATABASE", "skill_db")

    return (
        f"mysql+pymysql://{quote_plus(user)}:{quote_plus(password)}"
        f"@{host}:{port}/{name}"
    )


class Config:
    SQLALCHEMY_DATABASE_URI = _build_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {
        "connect_args": {"connect_timeout": 10},
    }

    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "change-this-secret")
    JWT_ACCESS_TOKEN_EXPIRES_MINUTES = int(
        os.getenv("JWT_ACCESS_TOKEN_EXPIRES_MINUTES", "60")
    )
