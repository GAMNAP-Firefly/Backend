from pydantic import BaseModel


class HRResultsRequest(BaseModel):
    access_key: str
