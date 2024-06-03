from fastapi import FastAPI
from src.lifespan import lifespan
from src.websockets.router import router as ws_router
from src.chats.views import router as chats_router
from src.messages.views import router as messages_router

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(ws_router)
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(messages_router, prefix="/chats/{chat_id}/messages", tags=["messages"])


@app.get("/")
def ping():
    return {"ping": "pong"}
