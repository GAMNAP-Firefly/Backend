from sqlalchemy.ext.asyncio import AsyncSession
from src.domain.repository.TestRepository import TestRepository
from src.domain.entity.Test import Test
from src.infrastructure.db.models.test_model import TestModel
from sqlalchemy import select
from typing import List

class SQLTestRepository(TestRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_test(self, test: Test) -> Test:
        """Добавить тест и вернуть созданную сущность."""
        db_test = TestModel(id=test.id, name=test.name, description=test.description)
        self.session.add(db_test)
        await self.session.commit()
        await self.session.refresh(db_test)  # Получаем данные с БД (включая автоинкремент)
        return Test(id=db_test.id, name=db_test.name, description=db_test.description)

    async def get_test(self, test_id) -> Test:
        """Получить тест с id."""
        db_test = await self.session.get(TestModel, test_id)
        if db_test:
            return Test(id=db_test.id, name=db_test.name, description=db_test.description)
        raise ValueError("Test not found")

    async def delete_test(self, test_id) -> None:
        """Удалить тест с id."""
        db_test = await self.session.get(TestModel, test_id)
        if db_test:
            await self.session.delete(db_test)
            await self.session.commit()
        else:
            raise ValueError("Test not found")

    async def edit_test(self, test_id, test: Test) -> None:
        """Изменить тест с id."""
        db_test = await self.session.get(TestModel, test_id)
        if db_test:
            db_test.name = test.name
            db_test.description = test.description
            await self.session.commit()
        else:
            raise ValueError("Test not found")

    async def get_all_tests(self) -> List[Test]:
        """Получить все тесты."""
        stmt = select(TestModel)
        result = await self.session.execute(stmt)
        db_tests = result.scalars().all()
        return [Test(id=t.id, name=t.name, description=t.description) for t in db_tests]