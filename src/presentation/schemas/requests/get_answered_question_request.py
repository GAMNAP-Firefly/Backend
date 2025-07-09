from pydantic import BaseModel

class GetAnsweredQuestionRequest(BaseModel):
    test_id: int
    question_id: int 