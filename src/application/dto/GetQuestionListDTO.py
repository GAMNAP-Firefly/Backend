from dataclasses import dataclass
from typing import List
from src.application.dto.VariantDTO import VariantDTO


@dataclass
class GetQuestionListDTO:
    id: int
