from fastapi import FastAPI
from src.lifespan import lifespan
from src.websockets.router import router as ws_router
from src.private_messenger.views import router as private_messenger_router

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(ws_router)
app.include_router(private_messenger_router, prefix="/chats", tags=["chats"])


@app.get("/")
def ping():
    return {"ping": "pong"}

