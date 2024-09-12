from fastapi import APIRouter

from chatgpt_retrieval_plugin.api.schemas.healthcheck import HealthCheck

router = APIRouter()


@router.get("/", response_model=HealthCheck)
def healthcheck() -> HealthCheck:
    return HealthCheck(status="OK")
