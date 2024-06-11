from fastapi import FastAPI
from src.lifespan import lifespan
from src.routers.chats import router as chats_router
from src.routers.group_messages import router as messages_router
from src.routers.websockets import router as ws_router

app = FastAPI(
    lifespan=lifespan,
)
app.include_router(ws_router, prefix="/ws")
app.include_router(chats_router, prefix="/chats", tags=["chats"])
app.include_router(
    messages_router, prefix="/chats/{chat_id}/messages", tags=["messages"]
)


@app.get("/")
def ping():
    return {"ping": "pong"}
