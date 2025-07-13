from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.User import User
from src.domain.repository.UserRepository import UserRepository
from src.infrastructure.db.models.user_model import UserModel


class SQLUserRepository(UserRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_user(self) -> User:
        """Добавить пользователя и вернуть созданную сущность."""
        db_user = UserModel()
        self.session.add(db_user)
        await self.session.commit()
        await self.session.refresh(db_user)  # Получаем данные с БД (включая автоинкремент)
        return User(id=db_user.id)

    async def get_user(self, user_id):
        """Получить пользователя с id."""
        db_user = await self.session.get(UserModel, user_id)
        if db_user:
            return User(id=db_user.id)
        raise ValueError("User not found")

    async def remove_user(self, user_id):
        """Удалить пользователя с id."""
        db_user = await self.session.get(UserModel, user_id)
        if db_user:
            await self.session.delete(db_user)
            await self.session.commit()
        else:
            raise ValueError("User not found")

    async def edit_user(self, user_id, user: User):
        """Изменить пользователя с id."""
        db_user = await self.session.get(UserModel, user_id)
        if db_user:
            db_user.id = user.id  # Поле id неизменяемо, но оставлено для консистентности
            await self.session.commit()
        else:
            raise ValueError("User not found")

    async def get_all_users(self) -> List[User]:
        """Получить всех пользователей."""
        stmt = select(UserModel)
        result = await self.session.execute(stmt)
        db_users = result.scalars().all()
        return [User(id=u.id) for u in db_users]
