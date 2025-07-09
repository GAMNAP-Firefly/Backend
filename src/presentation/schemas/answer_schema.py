from pydantic import BaseModel
from .question_schema import QuestionSchema
from .user_schema import UserSchema
from .variant_schema import VariantSchema
from .result_schema import ResultSchema

class AnswerSchema(BaseModel):
    question: QuestionSchema
    user: UserSchema
    variant: VariantSchema
    result: ResultSchema

    class Config:
        orm_mode = True 