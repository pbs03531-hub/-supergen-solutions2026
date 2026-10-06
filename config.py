import os


class Config:

    SECRET_KEY = os.getenv(
        "SECRET_KEY",
        "supergen-development-secret"
    )

    DATABASE_URL = os.getenv(
        "DATABASE_URL",
        "sqlite:///supergen.db"
    )

    # Render/PostgreSQL may provide postgres://
    # while SQLAlchemy expects postgresql://

    if DATABASE_URL.startswith("postgres://"):
        DATABASE_URL = DATABASE_URL.replace(
            "postgres://",
            "postgresql://",
            1
        )

    SQLALCHEMY_DATABASE_URI = DATABASE_URL

    SQLALCHEMY_TRACK_MODIFICATIONS = False