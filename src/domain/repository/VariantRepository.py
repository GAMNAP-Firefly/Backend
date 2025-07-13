from abc import ABC, abstractmethod
from typing import List

from src.domain.entity.Variant import Variant


class VariantRepository(ABC):
    @abstractmethod
    def add_variant(self, variant: Variant) -> Variant:
        """Добавить вариант и вернуть созданную сущность"""
        pass

    @abstractmethod
    def get_variant(self, variant_id: int) -> Variant:
        """Получить вариант с id"""
        pass

    @abstractmethod
    def remove_variant(self, variant_id: int) -> None:
        """Удалить вариант с id"""
        pass

    @abstractmethod
    def get_all_variants(self) -> List[Variant]:
        """Получить все варианты"""
        pass

    @abstractmethod
    def edit_variant(self, variant_id: int, variant: Variant) -> None:
        """Изменить вариант"""
        pass
