import logging
from src.application.dto.CategoryScoreDTO import CategoryScoreDTO
from src.application.dto.CreateUserDTO import CreateUserDTO
from src.domain.repository.UserRepository import UserRepository
from src.domain.entity.User import User
from src.application.service.jwt_service import JWTService


class CreateUserUseCase:
    """
    Use case создания нового пользователя.
    Создаёт нового пользователя, формирует и возвращает JWT-токен.
    """

    def __init__(self, user_repository: UserRepository, jwt_service: JWTService):
        self.user_repository = user_repository
        self.jwt_service = jwt_service

    async def execute(self) -> CreateUserDTO:
        """
        Выполняет use case.
        """
        logger = logging.getLogger(__name__)
        user = await self.user_repository.add_user()  # Создаем пользователя
        logger.info(f"Created user with ID: {user.id}")

        jwt_token = self.jwt_service.create_access_token(user_id=user.id)
        logger.info(f"Generated JWT token for user {user.id}")
        
        return CreateUserDTO(jwt_token=jwt_token)

