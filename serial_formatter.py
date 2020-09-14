"""Enter SAM data into a SQLite database. There are restrictions on the data that can be entered for example fictional
vendors"""
import re
import sqlite3
from sqlite3 import Error
import sam_db

# def main():
    #  RegEx search strings for certain software vendors
auto_ex = re.compile(r'\b(\d{3}-\d{8}\b)')
auto_key = re.compile(r'([a-zA-Z]|\d)\d([a-zA-Z]|\d)[a-zA-Z]\d')
abalo_ex = re.compile(r'(\b(\d{4}-){5}\d{4}\b)')


# Select from software vendor: Antidex, Abalobadiah, or None (None is temp. testing name)
# TODO: interface through PySimpleGUI or browser

def entering_func(inputly):
    """While loop with user and pre-determined exits as a decorator function"""
    done = "No"
    if len(software_vendors) == 0:
        max_entries = 13
    else:
        max_entries = len(software_vendors)
    while done.upper()[0] != "Y":
        inputly()
        if max_entries <= 1:
            print("I can't take anymore!")
            done = 'Y'
        # elif local index is out of range, exit loop
        else:
            done = input("Are you done making entries (y/n)? ")
            max_entries -= 1

def test_print(sn_event):
    print(sn_event)

software_vendors = []

# @entering_func
def soft_vend_enter():
    # global software_vendors
    vend_name = input("Enter one of the following two vendors: Antidex, Abalobadiah, or None: ")
    vend_amount = int(input(f"How many licenses do you have for {vend_name}? "))
    for amnt in range(vend_amount):
        software_vendors.append(vend_name)

# print(software_vendors)


# @entering_func
def sn_enter(sn_event, sn_sub_value):
    serials = []
    for serial in range(int(sn_sub_value)):
        serial = (input(f"Enter a serial number for {sn_event}: "))
        # if Antidex or Abalobadiah, s/n must match regex
        if sn_event == 'Antidex':
            while not re.match(auto_ex, serial):
                serial = (input(f"That is not a valid serial number for Antidex: "))
        if sn_event == 'Abalobadiah':
            while not re.match(abalo_ex, serial):
                serial = (input(f"That is not a valid serial number for Abalobadiah: "))
        serials.append((sn_event, serial))
    print(serials)
    # TODO: view serials, ask for confirmation to update db table, sam_db.update_table func()

pk_in = [None for x in range(len(software_vendors))]
# i = 0

# @entering_func
def pk_enter():
    # global pk_in
    i = 0
    if i < len(pk_in):
        pk_in[i] = (input(f"Enter a product key for {software_vendors[i]}, s/n: {serials[i]}: "))
        if software_vendors[i] == 'Antidex':
            while not re.match(auto_key, pk_in[i]):
                pk_in[i] = (input(f"That is not a valid product key for Antidex: "))
        i += 1

# print(pk_in)

"""
# prepare separate lists of tuples for separate database tables
all_licenses = list(zip(software_vendors, serials, pk_in))
anti_licenses = [license[1:3] for license in all_licenses if license[0] == 'Antidex']
abalo_licenses = [license[1:3] for license in all_licenses if license[0] == 'Abalobadiah']
none_licenses = [license[1:3] for license in all_licenses if (license[0] != 'Antidex' and license[0] != 'Abalobadiah')]
print('all: ', all_licenses)
print('anti: ', anti_licenses)
print('abalo: ', abalo_licenses)
print('none: ', none_licenses)

# conn = sam_db.create_connection(sam_db.create_connection('sam_records.db'))

if anti_licenses:
    sam_db.create_table(sam_db.sql_create_antidex_table)
if abalo_licenses:
    sam_db.create_table(sam_db.sql_create_abalobadiah_table)
if none_licenses:
    sam_db.create_table(sam_db.sql_create_none_table)
for vend_name in software_vendors:
    if (vend_name != 'Antidex') and (vend_name != 'Abalobadiah') and (vend_name != 'None'):
        sam_db.create_table((sam_db.sql_create_new_table, vend_name))
    """

# if __name__ == '__main__':
#     main()


# database funcs moved to sam_db.py
# def create_connection(db_file):
#     connect = None
#     try:
#         connect = sqlite3.connect(db_file)
#         print("connect success")
#         return connect
#     except Error as e:
#         print("connect failure", e)
#     finally:
#         return connect
#
#
# def create_table(conn, create_table_sql):
#     c = conn.cursor()
#     try:
#         c.execute(create_table_sql)
#         conn.commit()
#         print("table success(?)")
#     except Error as e:
#         print("create table error", e)
#     finally:
#         return c, conn
#
#
# def main():
#     database = "sam_records.db"
#     # make table for each vendor entered as create_table_sql
#     sql_create_antidex_table = "CREATE TABLE IF NOT EXISTS Antidex (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
#
#     sql_create_abalobadiah_table = "CREATE TABLE IF NOT EXISTS Abalobadiah (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
#
#     sql_create_none_table = "CREATE TABLE IF NOT EXISTS None (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"
#
#     conn = create_connection(database)
#
#     if conn is not None:
#         create_table(conn, sql_create_antidex_table)
#         create_table(conn, sql_create_abalobadiah_table)
#         create_table(conn, sql_create_none_table)
#     else:
#         print("Error creating database connection.")
#
#     c = conn.cursor()
#
#     c.executemany("INSERT INTO Antidex (s_n, [Product Key]) VALUES (?,?)", anti_licenses)
#     c.executemany("INSERT INTO Abalobadiah (s_n, [Product Key]) VALUES (?,?)", abalo_licenses)
#     c.executemany("INSERT INTO None (s_n, [Product Key]) VALUES (?,?)", none_licenses)
#
#     conn.commit()
#
#     c.execute("SELECT * FROM Antidex")
#     print('Antidex: ', c.fetchall())
#     c.execute("SELECT * FROM Abalobadiah")
#     print('Abalobadiah: ', c.fetchall())
#     c.execute("SELECT * FROM None")
#     print('None: ', c.fetchall())
#
#     conn.close()


