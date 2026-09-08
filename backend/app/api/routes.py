from fastapi import APIRouter
from app.config import settings
from app.schemas.health import HealthResponse

router = APIRouter()


@router.get(
    "/health",
    response_model=HealthResponse,
    summary="Backend Health Check",
    description="Returns backend status, service name, and API version."
)
async def get_health() -> HealthResponse:
    return HealthResponse(
        status="ok",
        service="ai-parallel-universe-backend",
        version=settings.APP_VERSION
    )
