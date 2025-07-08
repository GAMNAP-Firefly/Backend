from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Category import Category


class CategoryRepository(ABC):
    @abstractmethod
    def add_category(self, category: Category) -> None:
        """Добавить категорию"""
        pass

    @abstractmethod
    def get_category(self, category_id) -> Category:
        """Получить категорию с id"""
        pass

    @abstractmethod
    def remove_category(self, category_id: int) -> None:
        """Удалить категорию с id"""
        pass

    @abstractmethod
    def edit_category(self, category_id: int, category: Category) -> None:
        """Изменить категорию с id"""
        pass

    @abstractmethod
    def get_all_categories(self) -> List[Category]:
        """Получить все категории"""
        pass

    @abstractmethod
    def get_categories_by_ids(self, ids: list[int]) -> List[Category]:
        """Получить несколько категорий по списку их ID."""
        pass