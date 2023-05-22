from fastapi import APIRouter

from chatgpt_retrieval_plugin.api.endpoints import api

api_router: APIRouter = APIRouter()
api_router.include_router(
    api.router,
    tags=["chatgpt_retrieval_plugin"],
)
