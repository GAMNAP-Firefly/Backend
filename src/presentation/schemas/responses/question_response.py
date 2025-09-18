from typing import List

from pydantic import BaseModel


class VariantResponse(BaseModel):
    id: int
    text: str
    is_selected: bool = False


class QuestionResponse(BaseModel):
    id: int
    text: str
    index: int
    total: int
    progress_percent: float
    variants: List[VariantResponse]


class QuestionListResponse(BaseModel):
    questions_id: List[int]
