#!/usr/bin/env python3

from rich.console import Console
import structlog
from typer import Typer
import uvicorn

from chatgpt_retrieval_plugin.common.logging import initialize_logging

initialize_logging()
logger = structlog.get_logger()
app = Typer(add_completion=False)
console = Console()


@app.command()
def main() -> None:
    """Run training script"""
    console.print("Welcome to the owner relationship cli")


@app.command()
def server() -> None:
    """Run uvicorn server"""
    uvicorn.run(
        "chatgpt_retrieval_plugin.app:app",
        host="0.0.0.0",
        port=8000,
    )


if __name__ == "__main__":  # pragma: no cover
    app()
