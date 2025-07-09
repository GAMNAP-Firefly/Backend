from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from fastapi import HTTPException, status
from infrastructure.config.settings import settings


class JWTService:
    """Сервис для работы с JWT токенами."""
    
    def __init__(self):
        self.secret_key = settings.secret_key
        self.algorithm = settings.jwt_algorithm
        self.expire_minutes = settings.jwt_expire_minutes
    
    def create_access_token(self, data: dict, expires_delta: Optional[timedelta] = None) -> str:
        """
        Создает JWT токен доступа.
        
        Args:
            data: Данные для включения в токен
            expires_delta: Время жизни токена
            
        Returns:
            JWT токен
        """
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=self.expire_minutes)
        
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt
    
    def verify_token(self, token: str) -> dict:
        """
        Проверяет и декодирует JWT токен.
        
        Args:
            token: JWT токен
            
        Returns:
            Декодированные данные токена
            
        Raises:
            HTTPException: Если токен недействителен
        """
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
        except JWTError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Недействительный токен",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    def get_user_id_from_token(self, token: str) -> int:
        """
        Извлекает user_id из JWT токена.
        
        Args:
            token: JWT токен
            
        Returns:
            user_id из токена
        """
        payload = self.verify_token(token)
        user_id = payload.get("user_id")
        if user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Токен не содержит user_id",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return user_id


# Создаем экземпляр сервиса
jwt_service = JWTService() 