from typing import Optional

from fastapi import APIRouter, Body, File, Form, HTTPException, Request, UploadFile
import structlog

from chatgpt_retrieval_plugin.api.schemas.api import DeleteRequest, DeleteResponse, QueryRequest, QueryResponse, UpsertRequest, UpsertResponse
from chatgpt_retrieval_plugin.api.schemas.models import DocumentMetadata, Source
from chatgpt_retrieval_plugin.common.file import get_document_from_file

router = APIRouter()
logger = structlog.get_logger()


@router.post(
    "/upsert-file",
    response_model=UpsertResponse,
)
async def upsert_file(
    request: Request,
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
):
    try:
        metadata_obj = DocumentMetadata.parse_raw(metadata) if metadata else DocumentMetadata(source=Source.file)
    except Exception:
        metadata_obj = DocumentMetadata(source=Source.file)

    document = await get_document_from_file(file, metadata_obj)

    try:
        ids = await request.app.state.datastore.upsert([document])
        return UpsertResponse(ids=ids)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail=f"str({e})")


@router.post(
    "/upsert",
    response_model=UpsertResponse,
)
async def upsert(
    request: Request,
    data: UpsertRequest = Body(...),
):
    try:
        ids = await request.app.state.datastore.upsert(data.documents)
        return UpsertResponse(ids=ids)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@router.post(
    "/query",
    response_model=QueryResponse,
)
async def query_main(
    request: Request,
    data: QueryRequest = Body(...),
):
    try:
        results = await request.app.state.datastore.query(
            data.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@router.post(
    "/query",
    response_model=QueryResponse,
    # NOTE: We are describing the shape of the API endpoint input due to a current limitation in parsing arrays of objects from OpenAPI schemas. This will not be necessary in the future.
    description="Accepts search query objects array each with query and optional filter. Break down complex questions into sub-questions. Refine results by criteria, e.g. time / source, don't do this often. Split queries if ResponseTooLargeError occurs.",
)
async def query(
    request: Request,
    data: QueryRequest = Body(...),
):
    try:
        results = await request.app.state.datastore.query(
            data.queries,
        )
        return QueryResponse(results=results)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")


@router.delete(
    "/delete",
    response_model=DeleteResponse,
)
async def delete(
    request: Request,
    data: DeleteRequest = Body(...),
):
    if not (data.ids or data.filter or data.delete_all):
        raise HTTPException(
            status_code=400,
            detail="One of ids, filter, or delete_all is required",
        )
    try:
        success = await request.app.state.datastore.delete(
            ids=data.ids,
            filter=data.filter,
            delete_all=data.delete_all,
        )
        return DeleteResponse(success=success)
    except Exception as e:
        print("Error:", e)
        raise HTTPException(status_code=500, detail="Internal Service Error")
