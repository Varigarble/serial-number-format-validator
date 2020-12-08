import sqlite3
from collections import namedtuple
from dotenv import load_dotenv
from os import getenv

load_dotenv()
db = getenv('db_filepath')


def create_connection(db_file):
    connect = None
    try:
        connect = sqlite3.connect(db_file)
        print("connect success")
        return connect
    except sqlite3.Error as e:
        print("connect failure", e)
    finally:
        return connect


conn = create_connection(db)

# TODO: delete unused sql statements/make create_db, create_table funcs
sql_create_vendor_table = 'CREATE TABLE IF NOT EXISTS Vendors (id INTEGER PRIMARY KEY AUTOINCREMENT, Vendor TEXT, \
                            Serial_Number TEXT, Product_Key TEXT);'
sql_add_vendor = 'INSERT INTO Vendors (Vendor) VALUES (?);'
sql_update_vendor = 'UPDATE Vendors SET Vendor = ? WHERE Vendor = ?;'
sql_update_sn = 'UPDATE Vendors SET Serial_Number = ? WHERE id = ?;'
sql_update_product_key = 'UPDATE Vendors SET Product_Key = ? WHERE id = ?;'


def update_vendor(new, old):
    print(new, old)
    with conn:
        c = conn.cursor()
        c.execute(sql_update_vendor, (new, old))
        conn.commit()


def sn_pk_updater(set_out, sql_command):
    c = conn.cursor()
    for row in set_out:
        if sql_command == sql_update_sn:
            col = row.Serial_Number
        if sql_command == sql_update_product_key:
            col = row.Product_Key
        c.execute(sql_command, (col, row.id))
    conn.commit()


def create_table(create_table_sql, conn=conn):
    c = conn.cursor()
    try:
        c.execute(create_table_sql)
        conn.commit()
        print("table success(?)")
    except sqlite3.Error as e:
        print("create table error", e)
    finally:
        return c, conn


def view_vendors():
    with conn:
        vend_list = list(conn.cursor().execute("SELECT DISTINCT Vendor FROM Vendors ORDER BY Vendor"))
    return [vendor_tuple[0] for vendor_tuple in vend_list]


def view_all_none_sn_namedtuple():
    # get all entries w/out serial numbers from db && put in list type required by PySimpleGUI
    with conn:
        rows_list = []
        c = conn.cursor()
        c.execute("SELECT DISTINCT id, Vendor, Serial_Number, Product_Key FROM Vendors WHERE Serial_Number is NULL "
                  "ORDER BY Vendor")
        Row = namedtuple('Row', 'id, Vendor, Serial_Number, Product_Key')
        for row in map(Row._make, c.fetchall()):
            rows_list.append(row)
    return rows_list


def view_all_sn_namedtuple():
    # get all entries with serial numbers from db && put in list type required by PySimpleGUI
    with conn:
        rows_list = []
        c = conn.cursor()
        c.execute("SELECT DISTINCT id, Vendor, Serial_Number, Product_Key FROM Vendors WHERE Serial_Number is NOT NULL "
                  "ORDER BY Vendor")
        Row = namedtuple('Row', 'id, Vendor, Serial_Number, Product_Key')
        for row in map(Row._make, c.fetchall()):
            rows_list.append(row)
    return rows_list


def view_all_none_pk_namedtuple():
    # get all entries w/out product keys from db && put in list type required by PySimpleGUI
    with conn:
        rows_list = []
        c = conn.cursor()
        c.execute("SELECT id, Vendor, Serial_Number, Product_Key FROM Vendors WHERE Product_Key is NULL ORDER BY Vendor")
        Row = namedtuple('Row', 'id, Vendor, Serial_Number, Product_Key')
        for row in map(Row._make, c.fetchall()):
            rows_list.append(row)
    return rows_list


def view_all_pk_namedtuple():
    # get all entries with product keys from db && put in list type required by PySimpleGUI
    with conn:
        rows_list = []
        c = conn.cursor()
        c.execute("SELECT id, Vendor, Serial_Number, Product_Key FROM Vendors WHERE Product_Key is NOT NULL ORDER BY "
                  "Vendor")
        Row = namedtuple('Row', 'id, Vendor, Serial_Number, Product_Key')
        for row in map(Row._make, c.fetchall()):
            rows_list.append(row)
    return rows_list


def view_vendor_info(vendor_name):
    with conn:
        rows_list = []
        c = conn.cursor()
        c.execute("SELECT Vendor, Serial_Number, Product_Key FROM Vendors WHERE Vendor = ?;", (vendor_name[0],))
        Row = namedtuple('Row', 'Vendor, Serial_Number, Product_Key')
        for row in map(Row._make, c.fetchall()):
            rows_list.append(row)
    return rows_list


def soft_vend_enter(vend_name, amount):
    with conn:
        for amnt in range(amount):
            conn.execute(sql_add_vendor, (vend_name,))
    print(f"{amount} license(s) of {vend_name} added to database.")
