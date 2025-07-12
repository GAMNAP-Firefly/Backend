from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Result import Result


class ResultRepository(ABC):
    @abstractmethod
    def add_result(self, result: Result) -> None:
        """Добавить результат"""
        pass

    @abstractmethod
    def get_result_by_id(self, result_id: int) -> Result:
        """Получить результат с id"""
        pass

    @abstractmethod
    def get_user_test_result(self, user_id: int, test_id: int) -> Result:
        """Получить результат пользователя с id по тесту с id"""
        pass

    @abstractmethod
    def get_user_result(self, user_id: int) -> List[Result]:
        """Получить все результаты пользователя с id"""
        pass

    @abstractmethod
    def get_test_result(self, test_id: int) -> Result:
        """Получить все результаты по тесту с id"""
        pass

    @abstractmethod
    def delete_result_by_id(self, result_id: int) -> None:
        """Удалить результат по id"""
        pass

    @abstractmethod
    def delete_user_test_result(self, user_id: int, test_id: int) -> None:
        """Удалить результат пользователя с id по тесту с id"""
        pass

    @abstractmethod
    def edit_result_by_id(self, result_id: int, result: Result) -> None:
        """Изменить результат с id"""
        pass

    @abstractmethod
    def edit_user_test_result(self, user_id: int, test_id: int, result: Result) -> None:
        """Изменить вариант пользователя с id на тест с id"""
        pass

    @abstractmethod
    def get_all_results(self) -> List[Result]:
        """Получить все результаты"""
        pass

    @abstractmethod
    def get_result_by_token(self, link_token: str) -> Result:
        """Получить результат по токену-ссылке."""
        pass

    @abstractmethod
    def get_all_finished(self) -> List[Result]:
        """Получить все завершенные результаты."""
        pass

    @abstractmethod
    def get_test_id_by_token(self, link_token: str) -> int:
        """Получить ID теста по токену-ссылке."""
        pass
