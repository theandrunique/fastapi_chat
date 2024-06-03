
from fastapi import HTTPException, status

class ChatNotFound(HTTPException):
    def __init__(self, chat_id: str) -> None:
        super().__init__(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Chat {chat_id} not found",
        )

