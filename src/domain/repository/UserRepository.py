from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.User import User


class UserRepository(ABC):
    @abstractmethod
    def add_user(self, user: User):
        """Добавить пользователя"""
        pass

    @abstractmethod
    def get_user(self, user_id):
        """Получить пользователя с id"""
        pass

    @abstractmethod
    def remove_user(self, user_id):
        """Удалить пользователя с id"""
        pass

    @abstractmethod
    def edit_user(self, user_id, user: User):
        """Изменить пользователя с id"""
        pass

    @abstractmethod
    def get_all_users(self) -> List[User]:
        """Получить всех пользователей"""
        pass

