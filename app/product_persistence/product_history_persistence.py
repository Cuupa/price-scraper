import os
import sqlite3


class ProductHistoryPersistence:
    def __init__(self):
        self.database_file = "data/product.db"
        self.create_statement = """create table if not exists product_history (
                id_product integer not null,
                price text,
                currency text,
                date text not null
            );
        """

        self.index_statement = """create index if not exists 'index_id_product' on product_history(id_product);"""

        self.insert_statement = """insert into product_history(id_product, price, currency, date) 
        values (?, ?, ?, ?);
        """
        self.search_statement = """select id_product, price, currency, date from product_history where id_product=?;"""
        self.delete_by_id = """delete from product_history where id_product=?;"""
        self.init_db()

    def init_db(self):
        if not os.path.exists("data/"):
            os.makedirs("data/")
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.create_statement)
        cursor.execute(self.index_statement)
        con.commit()
        con.close()

    def search(self, product_id: int):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()

        cursor.execute(self.search_statement, (product_id,))
        rows = cursor.fetchall()
        return rows

    def insert(self, product_id: int, price: str, currency: str, date_time: str):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.insert_statement, (product_id, price, currency, date_time))
        con.commit()
        con.close()

    def remove(self, product_id):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.delete_by_id, (product_id,))
        con.commit()
        con.close()
