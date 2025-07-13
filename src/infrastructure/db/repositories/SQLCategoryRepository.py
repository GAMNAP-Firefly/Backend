from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repository.CategoryRepository import CategoryRepository
from src.domain.entity.Category import Category
from src.infrastructure.db.models.category_model import CategoryModel
from sqlalchemy import select
from typing import List

class SQLCategoryRepository(CategoryRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_category(self, category: Category) -> Category:
        """Добавить категорию и вернуть созданную сущность."""
        db_category = CategoryModel(id=category.id, name=category.name)
        self.session.add(db_category)
        await self.session.commit()
        await self.session.refresh(db_category)  # Получаем данные с БД (включая автоинкремент)
        return Category(id=db_category.id, name=db_category.name)

    async def get_category(self, category_id) -> Category:
        """Получить категорию с id."""
        db_category = await self.session.get(CategoryModel, category_id)
        if db_category:
            return Category(id=db_category.id, name=db_category.name)
        raise ValueError("Category not found")

    async def remove_category(self, category_id: int) -> None:
        """Удалить категорию с id."""
        db_category = await self.session.get(CategoryModel, category_id)
        if db_category:
            await self.session.delete(db_category)
            await self.session.commit()
        else:
            raise ValueError("Category not found")

    async def edit_category(self, category_id: int, category: Category) -> None:
        """Изменить категорию с id."""
        db_category = await self.session.get(CategoryModel, category_id)
        if db_category:
            db_category.name = category.name
            await self.session.commit()
        else:
            raise ValueError("Category not found")

    async def get_all_categories(self) -> List[Category]:
        """Получить все категории."""
        stmt = select(CategoryModel)
        result = await self.session.execute(stmt)
        db_categories = result.scalars().all()
        return [Category(id=c.id, name=c.name) for c in db_categories]

    async def get_categories_by_ids(self, ids: list[int]) -> List[Category]:
        """Получить несколько категорий по списку их ID."""
        stmt = select(CategoryModel).where(CategoryModel.id.in_(ids))
        result = await self.session.execute(stmt)
        db_categories = result.scalars().all()
        return [Category(id=c.id, name=c.name) for c in db_categories]