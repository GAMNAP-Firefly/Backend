from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.finish_test_use_case import FinishTestUseCase
from src.application.usecase.get_all_tests_use_case import GetAllTestsUseCase
from src.application.usecase.start_test_use_case import StartTestUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLAnswerRepository import SQLAnswerRepository
from src.infrastructure.db.repositories.SQLCategoryRepository import SQLCategoryRepository
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.presentation.schemas.requests.finish_test_request import FinishTestRequest
from src.presentation.schemas.requests.start_test_request import StartTestRequest
from src.presentation.schemas.responses.finish_test_response import FinishTestResponse, CategoryScoreResponse, \
    HRShareLinkResponse
from src.presentation.schemas.responses.test_list_response import TestListResponse, TestResponse

router = APIRouter(prefix="/test", tags=["Тесты"])


@router.get("/list", response_model=TestListResponse, status_code=status.HTTP_200_OK)
async def get_all_tests(
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetAllTestsUseCase(test_repo=SQLTestRepository(session))
    try:
        dtos = await use_case.execute()
        return TestListResponse(
            tests=[TestResponse(id=dto.id, name=dto.name, description=dto.description) for dto in dtos])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))


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


@router.post("/finish", response_model=FinishTestResponse, status_code=status.HTTP_200_OK)
async def finish_test(
        request: FinishTestRequest,
        session: AsyncSession = Depends(get_async_session)
):
    use_case = FinishTestUseCase(
        result_repo=SQLResultRepository(session),
        answer_repo=SQLAnswerRepository(session),
        category_repo=SQLCategoryRepository(session),
    )
    try:
        category_scores, hr_share_link = await use_case.execute(result_id=request.result_id)

        return FinishTestResponse(
            results=[CategoryScoreResponse(category_name=dto.category_name, score=dto.score) for dto in
                     category_scores],
            share_link=HRShareLinkResponse(share_code=hr_share_link.share_code)
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
