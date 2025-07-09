from pydantic import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fittin App"
    debug: bool = True
    database_url: str = "psql://postgres:postgres@db:5432/postgres"
    secret_key: str = "supersecretkey"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
