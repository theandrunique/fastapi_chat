from fastapi import FastAPI
from src.lifespan import lifespan
from src.websockets.router import router as ws_router

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(ws_router)


@app.get("/")
def ping():
    return {"ping": "pong"}

