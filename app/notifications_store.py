import os
import sqlite3

database_file = "data/notifications.db"
create_statement = """create table if not exists notification (
        id integer primary key,
        type text not null,
        url text not null,
        enabled integer not null
    );
"""

insert_statement = """insert into notification(type, url, enabled) values ("$value1", "$value2", $value3);"""
update_statement = """update notification set type="$value1", url="$value2", enabled=$value3 where id=$id"""
search_statement = """select id, type, url from notification where type="$value";"""

select_all = """select id, type, url, enabled from notification;"""
select_all_enabled = """select id, type, url, enabled from notification where enabled=1;"""


def init_db():
    if not os.path.exists("data/"):
        os.makedirs("data/")
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute(create_statement)
    con.commit()
    con.close()


def search(type: str):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = search_statement.replace("$value", type)
    cursor.execute(stmnt)
    rows = cursor.fetchall()
    return rows


def save(type: str, url: str, enabled: bool):
    init_db()

    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    notifications = search(type)

    if len(notifications) == 0:
        stmnt = (insert_statement.replace("$value1", type)
                 .replace("$value2", url)
                 .replace("$value3", "1" if enabled else "0"))
    else:
        stmnt = (update_statement.replace("$value1", type)
                 .replace("$value2", url)
                 .replace("$value3", "1" if enabled else "0")
                 .replace("$id", str(notifications[0][0])))

    cursor.execute(stmnt)
    con.commit()
    con.close()


def get_all_enabled():
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = select_all_enabled
    cursor.execute(stmnt)
    return cursor.fetchall()