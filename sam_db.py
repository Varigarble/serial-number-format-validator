import sqlite3
from sqlite3 import Error
# from typing import NamedTuple TODO: return sql query tuples as named?

# def main():


def create_connection(db_file):
    connect = None
    try:
        connect = sqlite3.connect(db_file)
        print("connect success")
        return connect
    except Error as e:
        print("connect failure", e)
    finally:
        return connect


conn = create_connection('sam_records.db')

"""Deprecated: separate tables for each vendor
# make table for each vendor entered as create_table_sql
sql_create_antidex_table = "CREATE TABLE IF NOT EXISTS Antidex (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_abalobadiah_table = "CREATE TABLE IF NOT EXISTS Abalobadiah (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_none_table = "CREATE TABLE IF NOT EXISTS None (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_new_table = "CREATE TABLE IF NOT EXISTS (New_Vendor) (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT) VALUES (?);"
"""

sql_create_vendor_table = "CREATE TABLE IF NOT EXISTS Vendors (id INTEGER PRIMARY KEY AUTOINCREMENT, Vendor TEXT, Serial_Number TEXT, Product_Key TEXT);"
sql_add_vendor = "INSERT INTO Vendors (Vendor) VALUES (?);"


def create_table(create_table_sql, conn=conn):
    c = conn.cursor()
    try:
        c.execute(create_table_sql)
        conn.commit()
        print("table success(?)")
    except Error as e:
        print("create table error", e)
    finally:
        return c, conn


def create_tables():
    if conn is not None:
        create_table(conn, sql_create_antidex_table)
        create_table(conn, sql_create_abalobadiah_table)
        create_table(conn, sql_create_none_table)

    else:
        print("Error creating database connection.")


# c = conn.cursor()


"""
c.executemany("INSERT INTO Antidex (s_n, [Product Key]) VALUES (?,?)", anti_licenses)
c.executemany("INSERT INTO Abalobadiah (s_n, [Product Key]) VALUES (?,?)", abalo_licenses)
c.executemany("INSERT INTO None (s_n, [Product Key]) VALUES (?,?)", none_licenses)

conn.commit()
"""


def view_vendors():
    with conn:
        c = conn.cursor()
        vend_list = list(c.execute("SELECT DISTINCT Vendor FROM Vendors ORDER BY Vendor"))
    return [vendor_tuple[0] for vendor_tuple in vend_list]


def view_sns():
    with conn:
        c = conn.cursor()
        sn_list = list(c.execute("SELECT Vendor, DISTINCT Serial_Number FROM Vendors ORDER BY Vendor"))
    return sn_list


def view_all():
    with conn:
        c = conn.cursor()
        all_list = list(c.execute("SELECT Vendor, Serial_Number, Product_Key FROM Vendors ORDER BY Vendor"))
    return all_list


def soft_vend_enter(vend_name):
    with conn:
        conn.execute("INSERT INTO Vendors (Vendor) VALUES (?);", (vend_name,))
    print("Never heard of 'em. Let me know when their IPO or SPAC is ready to take my money.")


def sn_write(sn_add_list):
    print(f"preparing to write {sn_add_list}")
    with conn:
        for entry in sn_add_list:
            conn.execute("INSERT INTO Vendors (Vendor, Serial_Number) VALUES (?, ?);", entry)


def update_table():
    pass





# if __name__ == '__main__':
#     main()