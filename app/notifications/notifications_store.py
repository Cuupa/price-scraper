import os
import sqlite3

from app.dataclasses.ntfy import ntfy


class NotificationsPersistence:
    def __init__(self):
        self.database_file = "data/notifications.db"
        self.ntfy_create_statement = """create table if not exists ntfy (
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

        self.ntfy_insert_statement = """insert into ntfy(
            url, 
            topic,
            enabled, 
            priority, 
            username, 
            password, 
            accesstoken
        ) values (?, ?, ?, ?, ?, ?, ?);"""
        self.ntfy_update_statement = """update ntfy set 
            url=?, 
            topic=?,
            enabled=?, 
            priority=?, 
            username=?, 
            password=?, 
            accesstoken=?
        where id=?;"""
        self.ntfy_select_statement = """select id, url, topic, enabled, priority, username, password, accesstoken from ntfy;"""
        self.init_db()

    def init_db(self):
        if not os.path.exists("data/"):
            os.makedirs("data/")
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.ntfy_create_statement)
        con.commit()
        con.close()

    def search(self, notification_type):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        stmnt = None
        if notification_type == 'ntfy':
            stmnt = self.ntfy_select_statement
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

    def save(self, notification: ntfy):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        existing_notification = search('ntfy')

        if existing_notification is None:
            cursor.execute(self.ntfy_insert_statement,
                           (notification.url,
                            notification.topic,
                            1 if notification.enabled else 0,
                            notification.priority,
                            notification.username,
                            notification.password,
                            notification.accesstoken))
        else:
            cursor.execute(self.ntfy_update_statement, (notification.url,
                                                        notification.topic,
                                                        1 if notification.enabled else 0,
                                                        notification.priority,
                                                        notification.username,
                                                        notification.password,
                                                        notification.accesstoken,
                                                        existing_notification.id))

        con.commit()
        con.close()
