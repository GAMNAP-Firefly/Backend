from pydantic import BaseModel


class CreateUserResponse(BaseModel):
    jwt_token: str
