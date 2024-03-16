import sqlite3

database_file = "product.db"
create_statement = """create table if not exists product_history (
        id_product integer not null,
        price text,
        currency text,
        date text not null
    );
"""

insert_statement = """insert into product_history(id_product, price, currency, date) 
values ($value1, "$value2", "$value3", "$value4");
"""

search_statement = """select id_product, price, currency, date from product_history where id_product=$value1;"""

delete_by_id = """delete from product_history where id_product=$value1;"""


def init_db():
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    cursor.execute(create_statement)
    con.commit()
    con.close()


def search(product_id: int):
    init_db()

    con = sqlite3.connect(database_file)
    cursor = con.cursor()

    stmnt = search_statement.replace("$value1", str(product_id))
    cursor.execute(stmnt)
    rows = cursor.fetchall()
    return rows


def insert(product_id: int, price: str, currency: str, date_time: str):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = (insert_statement.replace("$value1", str(product_id))
             .replace("$value2", price)
             .replace("$value3", currency)
             .replace("$value4", date_time))
    cursor.execute(stmnt)
    con.commit()
    con.close()


def remove(product_id):
    init_db()
    con = sqlite3.connect(database_file)
    cursor = con.cursor()
    stmnt = delete_by_id.replace("$value1", product_id)
    cursor.execute(stmnt)
    con.commit()
    con.close()
