import sqlite3

database_file = "product.db"
create_statement = """create table if not exists product (
        id integer primary key,
        url text not null,
        name text
    );
"""

insert_statement = """insert into product(url) values ("$value1");"""
search_statement = """select id, url, name from product where url="$value1";"""
all_statement = """select id, url, name from product;"""
id_statement = """select id, url, name from product where id=$value1"""

update_name_statement = """update product set name="$value1" where id=$value2;"""

delete_by_id = """delete from product where id=$value1;"""


def init_db():
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute(create_statement)
    con.commit()
    con.close()


def store_item(url: str) -> bool:
    init_db()
    success = False

    con = sqlite3.connect(database_file)
    cursor = con.cursor()

    if len(search(url)) == 0:
        stmnt = (insert_statement.replace("$value1", url))
        cursor.execute(stmnt)
        con.commit()
        success = True

    con.close()
    return success


def all_products():
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute(all_statement)
    return cursor.fetchall()


def search(url: str):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = search_statement.replace("$value1", url)
    cursor.execute(stmnt)
    rows = cursor.fetchall()
    return rows


def update(product_id: int, name: str):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = update_name_statement.replace("$value1", name).replace("$value2", str(product_id))
    cursor.execute(stmnt)
    con.commit()
    con.close()


def find(product_id):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = id_statement.replace("$value1", product_id)
    cursor.execute(stmnt)
    return cursor.fetchall()


def remove(product_id):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = delete_by_id.replace("$value1", product_id)
    cursor.execute(stmnt)
    con.commit()
    con.close()
