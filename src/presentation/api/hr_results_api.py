from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.usecase.get_all_hr_results_use_case import GetAllHRResultsUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository
from src.presentation.schemas.requests.hr_results_request import HRResultsRequest
from src.presentation.schemas.responses.hr_results_response import HRResultsListResponse, HRResultRowResponse

router = APIRouter(prefix="/hr", tags=["HRResults"])


@router.post("/results", response_model=HRResultsListResponse, status_code=status.HTTP_200_OK)
async def get_all_hr_results(
    request: HRResultsRequest,
    session: AsyncSession = Depends(get_async_session)
):
    use_case = GetAllHRResultsUseCase(result_repo=SQLResultRepository(session))
    try:
        dtos = use_case.execute(access_key=request.access_key)
        return HRResultsListResponse(results=[HRResultRowResponse(
            test_name=dto.test_name,
            start_time=dto.start_time,
            end_time=dto.end_time,
            link_token=dto.link_token
        ) for dto in dtos])
    except PermissionError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
