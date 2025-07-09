from fastapi import FastAPI

from src.infrastructure.config.settings import settings

app = FastAPI(title=settings.app_name, debug=settings.debug)
