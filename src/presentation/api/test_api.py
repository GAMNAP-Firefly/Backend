from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.start_test_use_case import StartTestUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.presentation.schemas.requests.start_test_request import StartTestRequest

router = APIRouter(prefix="/test", tags=["Тесты"])


@router.post("/start", status_code=status.HTTP_204_NO_CONTENT)
async def start_test(
        request: StartTestRequest,
        session: AsyncSession = Depends(get_async_session)
):
    use_case = StartTestUseCase(
        result_repo=SQLResultRepository(session),
    )
    try:
        await use_case.execute(result_id=request.result_id)

    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
