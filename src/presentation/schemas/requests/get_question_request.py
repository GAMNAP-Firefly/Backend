from pydantic import BaseModel


class GetQuestionRequest(BaseModel):
    test_id: int
    question_id: int
