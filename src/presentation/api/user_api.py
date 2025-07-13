from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.application.dto.CreateUserDTO import CreateUserDTO
from src.application.usecase.create_user_user_case import CreateUserUseCase
from src.application.service.jwt_service import JWTService
from src.infrastructure.db.database import get_async_session
from src.infrastructure.db.repositories.SQLUserRepository import SQLUserRepository
from src.presentation.schemas.responses.create_user_response import CreateUserResponse

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("", response_model=CreateUserResponse, status_code=status.HTTP_200_OK)
async def create_user(
        session: AsyncSession = Depends(get_async_session)
):
    jwt_service = JWTService()
    use_case = CreateUserUseCase(
        user_repository=SQLUserRepository(session=session),
        jwt_service=jwt_service
    )
    try:
        dto: CreateUserDTO = await use_case.execute()
        return CreateUserResponse(jwt_token=dto.jwt_token)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
