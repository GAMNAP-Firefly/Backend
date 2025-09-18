from pydantic import BaseModel

class CandidateAnalysisRequest(BaseModel):
    link_token: str 