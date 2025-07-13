from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.presentation.schemas.responses.candidate_analysis_response import CandidateAnalysisResponse
from src.presentation.schemas.requests.candidate_analysis_request import CandidateAnalysisRequest
from src.application.usecase.get_candidate_analysis_use_case import GetCandidateAnalysisUseCase
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLResultRepository import SQLResultRepository

router = APIRouter(prefix="/candidate-analysis", tags=["Анализ кандидатов"])

@router.post("/", response_model=CandidateAnalysisResponse, status_code=status.HTTP_200_OK)
async def get_candidate_analysis(
    request: CandidateAnalysisRequest,
    session: AsyncSession = Depends(get_async_session)
):
    use_case = GetCandidateAnalysisUseCase(result_repo=SQLResultRepository(session))
    try:
        dto = await use_case.execute(link_token=request.link_token)
        return CandidateAnalysisResponse(
            test_name=dto.test_name,
            start_time=dto.start_time,
            end_time=dto.end_time,
            duration_minutes=dto.duration_minutes,
            interpretation=dto.interpretation
        )
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e)) 