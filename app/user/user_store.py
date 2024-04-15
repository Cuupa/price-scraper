import os
import sqlite3

import hashlib
import uuid

from app.user.database_user import DatabaseUser


class UserPersistence:
    def __init__(self):
        self.database_file = "data/users.db"
        self.create_statement = """create table if not exists users (
            id integer primary key,
            username text not null,
            password text not null,
            salt text not null
        );    
        """

        self.insert_statement = """insert into users (username, password, salt) values(?, ?, ?);"""
        self.search_statement = """select username, password, salt from users where username=?;"""
        self.initdb()

    def initdb(self):
        if not os.path.exists("data/"):
            os.makedirs("data/")
        if not os.path.exists(self.database_file):
            connection = sqlite3.connect(self.database_file)

            connection.execute(self.create_statement)
            connection.commit()

            salt = uuid.uuid4().hex
            password = hashlib.sha512(salt.encode('utf-8') + "changeMe!".encode('utf-8')).hexdigest()
            connection.execute(self.insert_statement, ("admin", password, salt))
            connection.commit()
            connection.close()

    def search(self, username: str) -> DatabaseUser | None:
        con = sqlite3.connect(self.database_file)
        con.set_trace_callback(print)
        rows = con.execute(self.search_statement, (username,)).fetchall()
        con.close()
        for row in rows:
            return DatabaseUser(row[0], row[1], row[2])
        return None
