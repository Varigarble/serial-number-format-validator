import sqlite3
from sqlite3 import Error


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


# database = "sam_records.db"
# conn = create_connection(database)
conn = create_connection('sam_records.db')

# make table for each vendor entered as create_table_sql
sql_create_antidex_table = "CREATE TABLE IF NOT EXISTS Antidex (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_abalobadiah_table = "CREATE TABLE IF NOT EXISTS Abalobadiah (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_none_table = "CREATE TABLE IF NOT EXISTS None (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
sql_create_new_table = "CREATE TABLE IF NOT EXISTS (New_Vendor) (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT) VALUES (?);"


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

c = conn.cursor()
"""
c.executemany("INSERT INTO Antidex (s_n, [Product Key]) VALUES (?,?)", anti_licenses)
c.executemany("INSERT INTO Abalobadiah (s_n, [Product Key]) VALUES (?,?)", abalo_licenses)
c.executemany("INSERT INTO None (s_n, [Product Key]) VALUES (?,?)", none_licenses)

conn.commit()

c.execute("SELECT * FROM Antidex")
print('Antidex: ', c.fetchall())
c.execute("SELECT * FROM Abalobadiah")
print('Abalobadiah: ', c.fetchall())
c.execute("SELECT * FROM None")
print('None: ', c.fetchall())

conn.close()
"""

# if __name__ == '__main__':
#     main()