from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fittest"
    debug: bool = True
    database_url: str = "postgresql://postgres:postgres@localhost:5432/fittest"
    secret_key: str = "supersecretkey"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
