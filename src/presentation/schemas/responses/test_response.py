from pydantic import BaseModel
from typing import List
from src.presentation.schemas.responses.question_response import QuestionResponse


class VariantResponse(BaseModel):
    id: int
    text: str
    is_selected: bool = False


class StartTestResponse(BaseModel):
    result_id: int
    question: QuestionResponse
