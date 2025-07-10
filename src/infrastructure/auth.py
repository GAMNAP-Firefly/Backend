from typing import Annotated
from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from src.infrastructure.services.jwt_service import jwt_service

# Схема безопасности для JWT токенов
security = HTTPBearer()


def get_current_user_id(
    credentials: Annotated[HTTPAuthorizationCredentials, Depends(security)]
) -> int:
    """
    Dependency для извлечения user_id из JWT токена.
    
    Args:
        credentials: JWT токен из заголовка Authorization
        
    Returns:
        user_id из токена
        
    Raises:
        HTTPException: Если токен недействителен или отсутствует user_id
    """
    try:
        user_id = jwt_service.get_user_id_from_token(credentials.credentials)
        return user_id
    except HTTPException:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Недействительный токен аутентификации",
            headers={"WWW-Authenticate": "Bearer"},
        ) 