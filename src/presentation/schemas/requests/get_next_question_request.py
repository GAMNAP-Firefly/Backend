from pydantic import BaseModel

class GetNextQuestionRequest(BaseModel):
    test_id: int 