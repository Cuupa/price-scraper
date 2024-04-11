import bcrypt

from app.user import user_store


def is_authenticated(username: str, password: str):
    user = user_store.search(username)
    password_from_input = bcrypt.hashpw(password.encode('utf-8'), user.salt)
    if password_from_input == user.password:
        return True
    return False


def get(username):
    return user_store.search(username)