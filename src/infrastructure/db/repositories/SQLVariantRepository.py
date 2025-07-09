from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repository.VariantRepository import VariantRepository
from src.domain.entity.Variant import Variant
from src.infrastructure.db.models.variant_model import VariantModel
from sqlalchemy import select
from typing import List

class SQLVariantRepository(VariantRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_variant(self, variant: Variant) -> None:
        """Добавить вариант."""
        db_variant = VariantModel(id=variant.id, var_text=variant.var_text)
        self.session.add(db_variant)
        await self.session.commit()

    async def get_variant(self, variant_id: int) -> Variant:
        """Получить вариант с id."""
        db_variant = await self.session.get(VariantModel, variant_id)
        if db_variant:
            return Variant(id=db_variant.id, var_text=db_variant.var_text)
        raise ValueError("Variant not found")

    async def remove_variant(self, variant_id: int) -> None:
        """Удалить вариант с id."""
        db_variant = await self.session.get(VariantModel, variant_id)
        if db_variant:
            await self.session.delete(db_variant)
            await self.session.commit()
        else:
            raise ValueError("Variant not found")

    async def get_all_variants(self) -> List[Variant]:
        """Получить все варианты."""
        stmt = select(VariantModel)
        result = await self.session.execute(stmt)
        db_variants = result.scalars().all()
        return [Variant(id=v.id, var_text=v.var_text) for v in db_variants]

    async def edit_variant(self, variant_id: int, variant: Variant) -> None:
        """Изменить вариант."""
        db_variant = await self.session.get(VariantModel, variant_id)
        if db_variant:
            db_variant.var_text = variant.var_text
            await self.session.commit()
        else:
            raise ValueError("Variant not found")