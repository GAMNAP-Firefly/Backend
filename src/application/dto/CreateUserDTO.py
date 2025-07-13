from dataclasses import dataclass


@dataclass
class CreateUserDTO:
    jwt_token: str
