from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from starlette_prometheus import PrometheusMiddleware, metrics
import structlog

from chatgpt_retrieval_plugin.api.endpoints import healthcheck
from chatgpt_retrieval_plugin.api.router import api_router
from chatgpt_retrieval_plugin.config.settings import settings
from chatgpt_retrieval_plugin.data.milvus_datastore import MilvusDataStore

logger = structlog.get_logger()
app = FastAPI(
    title=settings.PROJECT_NAME,
    description="A retrieval API for querying and filtering documents based on natural language queries and metadata",
    version="0.1.0",
    openapi_url="/openapi.json",
)
app.mount("/.well-known", StaticFiles(directory=".well-known"), name="static")


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.add_middleware(PrometheusMiddleware)

app.add_route("/metrics", metrics)
app.include_router(healthcheck.router, tags=["health"])
app.include_router(api_router)


@app.on_event("startup")
async def startup() -> None:
    app.state.datastore = MilvusDataStore(create_new=False)
    logger.info("Chatgpt Retrieval Plugin service started.")


@app.on_event("shutdown")
async def shutdown() -> None:
    """Stop kafka clients."""
    logger.info("Chatgpt Retrieval Plugin service stopped.")
