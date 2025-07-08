from dataclasses import dataclass
from typing import List
from src.application.dto.VariantDTO import VariantDTO

@dataclass
class QuestionDTO:
    id: int
    text: str
    index: int
    total: int
    progress_percent: float
    variants: List[VariantDTO] 