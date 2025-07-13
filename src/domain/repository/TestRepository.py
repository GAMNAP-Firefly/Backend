from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Test import Test


class TestRepository(ABC):
    @abstractmethod
    def add_test(self, test: Test) -> Test:
        """Добавить тест и вернуть созданную сущность"""

    @abstractmethod
    def get_test(self, test_id) -> Test:
        """Получить тест с id"""
        pass

    @abstractmethod
    def delete_test(self, test_id) -> None:
        """Удалить тест с id"""
        pass

    @abstractmethod
    def edit_test(self, test_id, test: Test) -> None:
        """Изменить тест с id"""
        pass

    @abstractmethod
    def get_all_tests(self) -> List[Test]:
        """Получить все тесты"""
        pass
