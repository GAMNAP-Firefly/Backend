from pydantic import BaseModel

class HRResultsByLinkRequest(BaseModel):
    share_code: str 