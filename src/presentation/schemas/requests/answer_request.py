from pydantic import BaseModel

class SubmitAnswerRequest(BaseModel):
    question_id: int
    variant_id: int
    result_id: int 