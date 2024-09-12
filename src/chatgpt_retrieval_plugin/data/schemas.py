from pymilvus import DataType, FieldSchema

from chatgpt_retrieval_plugin.config.settings import settings


class Required:
    pass


SCHEMA_V1 = [
    (
        "pk",
        FieldSchema(
            name="pk",
            dtype=DataType.INT64,
            is_primary=True,
            auto_id=True,
        ),
        Required,
    ),
    (
        settings.EMBEDDING_FIELD,
        FieldSchema(
            name=settings.EMBEDDING_FIELD,
            dtype=DataType.FLOAT_VECTOR,
            dim=settings.OUTPUT_DIM,
        ),
        Required,
    ),
    (
        "text",
        FieldSchema(name="text", dtype=DataType.VARCHAR, max_length=65535),
        Required,
    ),
    (
        "document_id",
        FieldSchema(
            name="document_id",
            dtype=DataType.VARCHAR,
            max_length=65535,
        ),
        "",
    ),
    (
        "source_id",
        FieldSchema(name="source_id", dtype=DataType.VARCHAR, max_length=65535),
        "",
    ),
    (
        "id",
        FieldSchema(
            name="id",
            dtype=DataType.VARCHAR,
            max_length=65535,
        ),
        "",
    ),
    (
        "source",
        FieldSchema(name="source", dtype=DataType.VARCHAR, max_length=65535),
        "",
    ),
    (
        "url",
        FieldSchema(name="url", dtype=DataType.VARCHAR, max_length=65535),
        "",
    ),
    ("created_at", FieldSchema(name="created_at", dtype=DataType.INT64), -1),
    (
        "author",
        FieldSchema(name="author", dtype=DataType.VARCHAR, max_length=65535),
        "",
    ),
]

# V2 schema, remomve the "pk" field
SCHEMA_V2 = SCHEMA_V1[1:]
SCHEMA_V2[4][1].is_primary = True
