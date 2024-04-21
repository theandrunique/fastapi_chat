from fastapi import HTTPException


class ChatNotFound(HTTPException):
    def __init__(self) -> None:
        super().__init__(status_code=404, detail="Chat not found")
