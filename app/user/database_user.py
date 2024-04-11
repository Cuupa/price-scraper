class DatabaseUser():
    def __init__(self, email, password, salt):
        self.id = email
        self.password = password
        self.salt = salt
