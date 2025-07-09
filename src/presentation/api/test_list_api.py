from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.get_all_tests_use_case import GetAllTestsUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLTestRepository import SQLTestRepository
from src.presentation.schemas.requests.test_list_request import TestListRequest
from src.presentation.schemas.responses.test_list_response import TestListResponse, TestResponse

router = APIRouter(prefix="/tests", tags=["Tests"])


@router.post("/list", response_model=TestListResponse, status_code=status.HTTP_200_OK)
async def get_all_tests(
        request: TestListRequest,
        session: AsyncSession = Depends(get_async_session)
):
    use_case = GetAllTestsUseCase(test_repo=SQLTestRepository(session))
    try:
        dtos = await use_case.execute()
        return TestListResponse(
            tests=[TestResponse(id=dto.id, name=dto.name, description=dto.description) for dto in dtos])
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
