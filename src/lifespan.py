from contextlib import asynccontextmanager

from fastapi import FastAPI

from typing import Any

from src.mongo import test_connection


async def on_startup(app: FastAPI) -> None:
    await test_connection()


async def on_shutdown(app: FastAPI) -> None: ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    await on_startup(app)
    yield
    await on_shutdown(app)
