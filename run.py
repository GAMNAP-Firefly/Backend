#!/usr/bin/env python3
"""
Скрипт для запуска FastAPI приложения.
"""

import sys
from pathlib import Path

# Добавляем src в Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path))

if __name__ == "__main__":
    import uvicorn

    print("🚀 Запуск Fittest Backend...")
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
