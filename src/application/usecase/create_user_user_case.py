from src.application.dto.CategoryScoreDTO import CategoryScoreDTO
from src.application.dto.CreateUserDTO import CreateUserDTO
from src.domain.repository.UserRepository import UserRepository
from src.main import jwt_service


class CreateUserUseCase:
    """
    Use case создания нового пользователя.
    Создаёт нового пользователя, формирует и возвращает JWT-токен.
    """

    def __init__(self, user_repository: UserRepository):
        self.user_repository = user_repository

    async def execute(self) -> CreateUserDTO:
        """
        Выполняет use case.

        """

        user = self.user_repository.add_user()

        return CreateUserDTO(
            jwt_token=jwt_service.create_access_token(user_id=user.id)
        )

