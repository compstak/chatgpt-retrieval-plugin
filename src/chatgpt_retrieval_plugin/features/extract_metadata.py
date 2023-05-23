import json
from typing import Dict

from chatgpt_retrieval_plugin.api.schemas.models import Source
from chatgpt_retrieval_plugin.features.openai import get_chat_completion


def extract_metadata_from_document(text: str) -> Dict[str, str]:
    sources = Source.__members__.keys()
    sources_string = ", ".join(sources)
    # This prompt is just an example, change it to fit your use case
    messages = [
        {
            "role": "system",
            "content": f"""
            Given a document from a user, try to extract the following metadata:
            - source: string, one of {sources_string}
            - url: string or don't specify
            - created_at: string or don't specify
            - author: string or don't specify

            Respond with a JSON containing the extracted metadata in key value pairs. If you don't find a metadata field, don't specify it.
            """,
        },
        {"role": "user", "content": text},
    ]

    completion = get_chat_completion(
        messages,
        "gpt-4",
    )  # TODO: change to your preferred model name

    print(f"completion: {completion}")

    try:
        metadata = json.loads(completion)
    except Exception:
        metadata = {}

    return metadata