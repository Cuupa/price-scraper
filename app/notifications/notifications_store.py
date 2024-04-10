import os
import sqlite3

from app.dataclasses.ntfy import ntfy

database_file = "data/notifications.db"
ntfy_create_statement = """create table if not exists ntfy (
        id integer primary key,
        url text not null,
        topic text not null,
        enabled integer not null,
        priority integer not null,
        username text,
        password blob,
        accesstoken blob
    );
"""

ntfy_insert_statement = """insert into ntfy(
    url, 
    topic,
    enabled, 
    priority, 
    username, 
    password, 
    accesstoken
) values (?, ?, ?, ?, ?, ?, ?);"""
ntfy_update_statement = """update ntfy set 
    url=?, 
    topic=?,
    enabled=?, 
    priority=?, 
    username=?, 
    password=?, 
    accesstoken=?
where id=?;"""
ntfy_select_statement = """select id, url, topic, enabled, priority, username, password, accesstoken from ntfy;"""


def init_db():
    if not os.path.exists("data/"):
        os.makedirs("data/")
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute(ntfy_create_statement)
    con.commit()
    con.close()


def search(notification_type):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = None
    if notification_type == 'ntfy':
        stmnt = ntfy_select_statement
    cursor.execute(stmnt)
    rows = cursor.fetchall()
    if len(rows) == 0:
        return None
    return ntfy(id=rows[0][0],
                url=rows[0][1],
                topic=rows[0][2],
                enabled=rows[0][3],
                priority=rows[0][4],
                username=rows[0][5],
                password=rows[0][6],
                accesstoken=rows[0][7])


def save(notification: ntfy):
    init_db()

    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    existing_notification = search('ntfy')

    if existing_notification is None:
        cursor.execute(ntfy_insert_statement,
                       (notification.url,
                        notification.topic,
                        1 if notification.enabled else 0,
                        notification.priority,
                        notification.username,
                        notification.password,
                        notification.accesstoken))
    else:
        cursor.execute(ntfy_update_statement, (notification.url,
                                               notification.topic,
                                               1 if notification.enabled else 0,
                                               notification.priority,
                                               notification.username,
                                               notification.password,
                                               notification.accesstoken,
                                               existing_notification.id))

    con.commit()
    con.close()
