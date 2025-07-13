from typing import List

from pydantic import BaseModel


class GetQuestionVariantResponse(BaseModel):
    id: int
    text: str
    is_selected: bool = False


class GetQuestionResponse(BaseModel):
    id: int
    text: str
    variants: List[GetQuestionVariantResponse]
