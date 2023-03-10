import uuid


def get_random_password() -> str:
    return str(uuid.uuid4())
