import sys
import os
from pathlib import Path

# Добавляем src в Python path
src_path = Path(__file__).parent / "src"
sys.path.insert(0, str(src_path)) 