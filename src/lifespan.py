from contextlib import asynccontextmanager

from fastapi import FastAPI

from typing import AsyncIterator


async def on_startup(app: FastAPI) -> None: ...


async def on_shutdown(app: FastAPI) -> None: ...


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator:
    await on_startup(app)
    yield
    await on_shutdown(app)
