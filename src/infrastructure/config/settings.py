from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    app_name: str = "Fittest"
    debug: bool = True
    database_url: str = "postgresql+asyncpg://postgres:postgres@localhost:5432/fittest"
    secret_key: str = "supersecretkey"
    
    # Настройки логирования
    log_level: str = "INFO"
    log_file: str = ""
    
    # Настройки JWT
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 30
    
    # Настройки CORS
    cors_origins: list = ["*"]
    cors_allow_credentials: bool = True
    cors_allow_methods: list = ["*"]
    cors_allow_headers: list = ["*"]

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


settings = Settings()
