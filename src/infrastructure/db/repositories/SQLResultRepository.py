from typing import List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.domain.entity.Result import Result
from src.domain.entity.Test import Test
from src.domain.entity.User import User
from src.domain.repository.ResultRepository import ResultRepository
from src.infrastructure.db.models.result_model import ResultModel


class SQLResultRepository(ResultRepository):
    def __init__(self, session: AsyncSession):
        self.session = session

    async def add_result(self, result: Result) -> None:
        """Добавить результат."""
        db_result = ResultModel(
            user_id=result.user.id,
            test_id=result.test.id,
            start_time=result.start_time,
            end_time=result.end_time,
            status=result.status,
            link_token=result.link_token,
            interpretation=result.interpretation
        )
        self.session.add(db_result)
        await self.session.commit()

    async def get_result_by_id(self, result_id: int) -> Result:
        """Получить результат с id."""
        db_result = await self.session.get(ResultModel, result_id)
        if db_result:
            return Result(
                id=db_result.id,
                user=User(id=db_result.user_id),
                test=Test(id=db_result.test_id, name="", description=""),
                start_time=db_result.start_time,
                end_time=db_result.end_time,
                status=db_result.status,
                link_token=db_result.link_token,
                interpretation=db_result.interpretation
            )
        raise ValueError("Result not found")

    async def get_user_test_result(self, user_id: int, test_id: int) -> Result:
        """Получить результат пользователя с id по тесту с id."""
        stmt = select(ResultModel).where(
            ResultModel.user_id == user_id,
            ResultModel.test_id == test_id
        )
        result = await self.session.execute(stmt)
        db_result = result.scalar_one_or_none()
        if db_result:
            return Result(
                id=db_result.id,
                user=User(id=db_result.user_id),
                test=Test(id=db_result.test_id, name="", description=""),
                start_time=db_result.start_time,
                end_time=db_result.end_time,
                status=db_result.status,
                link_token=db_result.link_token,
                interpretation=db_result.interpretation
            )
        raise ValueError("Result not found")

    async def get_user_result(self, user_id: int) -> List[Result]:
        """Получить все результаты пользователя с id."""
        stmt = select(ResultModel).where(ResultModel.user_id == user_id)
        result = await self.session.execute(stmt)
        db_results = result.scalars().all()
        return [
            Result(
                id=r.id,
                user=User(id=r.user_id),
                test=Test(id=r.test_id, name="", description=""),
                start_time=r.start_time,
                end_time=r.end_time,
                status=r.status,
                link_token=r.link_token,
                interpretation=r.interpretation
            ) for r in db_results
        ]

    async def get_test_result(self, test_id: int) -> Result:
        """Получить все результаты по тесту с id (возвращает первый, если несколько)."""
        stmt = select(ResultModel).where(ResultModel.test_id == test_id)
        result = await self.session.execute(stmt)
        db_result = result.scalar_one_or_none()
        if db_result:
            return Result(
                id=db_result.id,
                user=User(id=db_result.user_id),
                test=Test(id=db_result.test_id, name="", description=""),
                start_time=db_result.start_time,
                end_time=db_result.end_time,
                status=db_result.status,
                link_token=db_result.link_token,
                interpretation=db_result.interpretation
            )
        raise ValueError("Result not found")

    async def delete_result_by_id(self, result_id: int) -> None:
        """Удалить результат по id."""
        db_result = await self.session.get(ResultModel, result_id)
        if db_result:
            await self.session.delete(db_result)
            await self.session.commit()
        else:
            raise ValueError("Result not found")

    async def delete_user_test_result(self, user_id: int, test_id: int) -> None:
        """Удалить результат пользователя с id по тесту с id."""
        stmt = select(ResultModel).where(
            ResultModel.user_id == user_id,
            ResultModel.test_id == test_id
        )
        result = await self.session.execute(stmt)
        db_result = result.scalar_one_or_none()
        if db_result:
            await self.session.delete(db_result)
            await self.session.commit()
        else:
            raise ValueError("Result not found")

    async def edit_result_by_id(self, result_id: int, result: Result) -> None:
        """Изменить результат с id."""
        db_result = await self.session.get(ResultModel, result_id)
        if db_result:
            db_result.user_id = result.user.id
            db_result.test_id = result.test.id
            db_result.start_time = result.start_time
            db_result.end_time = result.end_time
            db_result.status = result.status
            db_result.link_token = result.link_token
            db_result.interpretation = result.interpretation
            await self.session.commit()
        else:
            raise ValueError("Result not found")

    async def edit_user_test_result(self, user_id: int, test_id: int, result: Result) -> None:
        """Изменить вариант пользователя с id на тест с id."""
        stmt = select(ResultModel).where(
            ResultModel.user_id == user_id,
            ResultModel.test_id == test_id
        )
        db_result = (await self.session.execute(stmt)).scalar_one_or_none()
        if db_result:
            db_result.user_id = result.user.id
            db_result.test_id = result.test.id
            db_result.start_time = result.start_time
            db_result.end_time = result.end_time
            db_result.status = result.status
            db_result.link_token = result.link_token
            db_result.interpretation = result.interpretation
            await self.session.commit()
        else:
            raise ValueError("Result not found")

    async def get_all_results(self) -> List[Result]:
        """Получить все результаты."""
        stmt = select(ResultModel)
        result = await self.session.execute(stmt)
        db_results = result.scalars().all()
        return [
            Result(
                id=r.id,
                user=User(id=r.user_id),
                test=Test(id=r.test_id, name="", description=""),
                start_time=r.start_time,
                end_time=r.end_time,
                status=r.status,
                link_token=r.link_token,
                interpretation=r.interpretation
            ) for r in db_results
        ]

    async def get_result_by_token(self, link_token: str) -> Result:
        """Получить результат по токену-ссылке."""
        stmt = select(ResultModel).where(ResultModel.link_token == link_token)
        result = await self.session.execute(stmt)
        db_result = result.scalar_one_or_none()
        if db_result:
            return Result(
                id=db_result.id,
                user=User(id=db_result.user_id),
                test=Test(id=db_result.test_id, name="", description=""),
                start_time=db_result.start_time,
                end_time=db_result.end_time,
                status=db_result.status,
                link_token=db_result.link_token,
                interpretation=db_result.interpretation
            )
        raise ValueError("Result not found")

    async def get_all_finished(self) -> List[Result]:
        """Получить все завершенные результаты."""
        stmt = select(ResultModel).where(ResultModel.status == "finished")
        result = await self.session.execute(stmt)
        db_results = result.scalars().all()
        return [
            Result(
                id=r.id,
                user=User(id=r.user_id),
                test=Test(id=r.test_id, name="", description=""),
                start_time=r.start_time,
                end_time=r.end_time,
                status=r.status,
                link_token=r.link_token,
                interpretation=r.interpretation
            ) for r in db_results
        ]

    async def get_test_id_by_token(self, link_token: str) -> int:
        """Получить ID теста по токену-ссылке."""
        result = await self.get_result_by_token(link_token)
        return result.test.id
