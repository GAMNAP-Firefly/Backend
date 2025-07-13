from dataclasses import dataclass
from typing import List


@dataclass
class QuestionVariantDTO:
    id: int
    text: str
    is_selected: bool


@dataclass
class GetQuestionDTO:
    id: int
    text: str
    variants: List[QuestionVariantDTO]
