

def get_chat_id(from_id: str, to_id: str) -> str:
    return f"chat_{from_id}_{to_id}" if int(from_id) < int(to_id) else f"chat_{to_id}_{from_id}"