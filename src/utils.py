from uuid import UUID


def get_topic_name(user_id: UUID) -> str:
    return f"user_{user_id.hex}"
