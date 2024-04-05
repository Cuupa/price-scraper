from app import notifications_store


def notify(payload: str):
    pass


def register(type: str, url: str, enabled: bool):
    notifications_store.save(type, url, enabled)
