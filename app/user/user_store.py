import os
import sqlite3

import bcrypt

from app.user.database_user import DatabaseUser

database_file = "data/users.db"
create_statement = """create table if not exists users (
    id integer primary key,
    username text not null,
    password text not null,
    salt text not null
);    
"""

insert_statement = """insert into users (username, password, salt) values(?, ?, ?);"""
search_statement = """select username, password, salt from users where username=?;"""


def initdb():
    if not os.path.exists("data/"):
        os.makedirs("data/")
    if not os.path.exists(database_file):
        connection = sqlite3.connect(database_file)

        cursor = connection.cursor()
        cursor.execute(create_statement)
        connection.commit()
        cursor.close()

        salt = bcrypt.gensalt(12)
        password = bcrypt.hashpw("changeMe!".encode('utf-8'), salt)
        cursor.execute(insert_statement, (
        "admin", str(password).replace('b', '').replace('\'', ''), str(salt).replace('b', '').replace('\'', '')))
        cursor.close()
        connection.commit()
        connection.close()


def search(username: str):
    initdb()
    con = sqlite3.connect(database_file)
    con.set_trace_callback(print)
    cursor = con.cursor()
    con.execute(search_statement, (username,))
    rows = cursor.fetchall()
    cursor.close()
    con.close()
    users = []
    for row in rows:
        user = DatabaseUser(row[1], row[2], row[3])
        users.append(user)
    return users
