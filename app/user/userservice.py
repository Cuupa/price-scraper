import hashlib

from app.flaskuser import FlaskUser
from app.user.user_store import UserPersistence

user_store = UserPersistence()


def is_authenticated(user: FlaskUser) -> bool:
    database_user = user_store.search(user.id)
    if user is not None:
        password_from_input = hashlib.sha512(
            database_user.salt.encode('utf-8') + user.password.encode('utf-8')).hexdigest()
        if password_from_input == database_user.password:
            return True
    return False


def get(username) -> FlaskUser:
    database_user = user_store.search(username)
    return FlaskUser(database_user.username, database_user.password)
