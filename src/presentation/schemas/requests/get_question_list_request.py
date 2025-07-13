from pydantic import BaseModel


class GetQuestionListRequest(BaseModel):
    test_id: int
