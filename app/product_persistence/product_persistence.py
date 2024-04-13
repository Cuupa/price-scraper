import os.path
import sqlite3


class ProductPersistence:
    def __init__(self):
        self.database_file = "data/product.db"
        self.create_statement = """create table if not exists product (
                id integer primary key,
                url text not null,
                name text
            );
        """

        self.insert_statement = """insert into product(url) values (?);"""
        self.search_statement = """select id, url, name from product where url=?;"""
        self.all_statement = """select id, url, name from product;"""
        self.id_statement = """select id, url, name from product where id=?;"""

        self.update_name_statement = """update product set name="$value1" where id=?;"""

        self.delete_by_id = """delete from product where id=?;"""
        self.init_db()

    def init_db(self):
        if not os.path.exists("data/"):
            os.makedirs("data/")
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.create_statement)
        con.commit()
        con.close()

    def store_item(self, url: str) -> bool:
        success = False

        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()

        if len(search(url)) == 0:
            cursor.execute(self.insert_statement, (url,))
            con.commit()
            success = True

        con.close()
        return success

    def all_products(self):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.all_statement)
        return cursor.fetchall()

    def search(self, url: str):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.search_statement, (url,))
        rows = cursor.fetchall()
        return rows

    def update(self, product_id: int, name: str):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.update_name_statement, (name, product_id))
        con.commit()
        con.close()

    def find(self, product_id):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.id_statement, (product_id,))
        return cursor.fetchall()

    def remove(self, product_id):
        con = sqlite3.connect(self.database_file)
        cursor = con.cursor()
        cursor.execute(self.delete_by_id, (product_id,))
        con.commit()
        con.close()
