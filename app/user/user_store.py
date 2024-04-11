import os
import sqlite3

import bcrypt

from app.user.database_user import DatabaseUser

database_file = "data/users.db"
create_statement = """create table if not exists user (
    id integer primary key,
    username text not null,
    password text not null,
    salt text not null
);    
"""

create_dummy_user = """insert into user (username, password, salt) values(?, ?, ?);"""
insert_statement = """insert into user(username, password, salt) values(?,?,?);"""
search_statement = """select username, password, salt from user where username=?;"""


def initdb():
    if not os.path.exists("data/"):
        os.makedirs("data/")
    if not os.path.exists(database_file):
        con = sqlite3.connect(database_file)
        cursor = con.cursor()
        cursor.execute(create_statement)

        salt = bcrypt.gensalt(12)
        password = bcrypt.hashpw("changeMe!".encode('utf-8'), salt)
        cursor.execute(create_dummy_user, ("admin", password, salt))
        con.commit()
        con.close()


def search(username: str):
    initdb()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    con.execute(search_statement, username)
    rows = cursor.fetchall()
    users = []
    for row in rows:
        user = DatabaseUser(row[1], row[2], row[3])
        users.append(user)
    return users
