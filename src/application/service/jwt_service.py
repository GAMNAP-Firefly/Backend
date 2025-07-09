import jwt
from fastapi import Request, HTTPException, status, Depends
from infrastructure.config.settings import settings

SECRET_KEY = settings.secret_key
ALGORITHM = "HS256"

class JWTService:
    @staticmethod
    def create_access_token(user_id: int) -> str:
        payload = {"user_id": user_id}
        token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
        return token

    @staticmethod
    def decode_access_token(token: str) -> dict:
        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            return payload
        except jwt.PyJWTError:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token")

# FastAPI dependency для получения user_id из JWT
async def get_current_user_id(request: Request) -> int:
    auth_header = request.headers.get("Authorization")
    if not auth_header or not auth_header.startswith("Bearer "):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Missing or invalid Authorization header")
    token = auth_header.split(" ", 1)[1]
    payload = JWTService.decode_access_token(token)
    user_id = payload.get("user_id")
    if user_id is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    return user_id 