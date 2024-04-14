class DatabaseUser():
    def __init__(self, username, password, salt):
        self.username = username
        self.password = password
        self.salt = salt
