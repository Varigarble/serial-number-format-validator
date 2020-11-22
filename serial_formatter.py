"""Enter SAM data into a SQLite database. There are restrictions on the data that can be entered for example fictional
vendors"""
import re
import sqlite3
from sqlite3 import Error
import sam_db
import PySimpleGUI as sg

# def main():
#  RegEx search strings for certain software vendors
anti_ex = re.compile(r'\b(\d{3}-\d{8}\b)')
anti_key = re.compile(r'\b([a-zA-Z]|\d)\d([a-zA-Z]|\d)[a-zA-Z]\d\b')
abalo_ex = re.compile(r'(\b(\d{4}-){5}\d{4}\b)')
jj_key = re.compile(r'\b\d{3}\b')

serial_number_restrictions = {'Antidex': anti_ex, 'Abalobadiah': abalo_ex}
product_key_restrictions = {'Antidex': anti_key, 'jj': jj_key}
# Select from software vendor: Antidex, Abalobadiah, or None (None is temp. testing name)


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


def sn_enter(sn_event="Test (actual comes from sam_gui)", sn_amount=2):
    serials = []
    for serial in range(int(sn_amount)):
        # TODO: Can this be rewritten as a generator for contextlib.contextmanager?
        serial = sg.popup_get_text(f"Enter a serial number for {sn_event}: ")
        # if Antidex or Abalobadiah, s/n must match regex
        if sn_event == 'Antidex':
            while not re.match(anti_ex, serial):
                serial = sg.popup_get_text(f"That is not a valid serial number for Antidex: ")
        if sn_event == 'Abalobadiah':
            while not re.match(abalo_ex, serial):
                serial = sg.popup_get_text(f"That is not a valid serial number for Abalobadiah: ")
        serials.append((sn_event, serial))
    return serials  # go back to sam_gui.py for confirmation


pk_in = [None for x in range(len(software_vendors))]


def pk_checker(row, initial_key):
    if row is None:
        row = ''
    if initial_key is None:
        initial_key = ''
    if row[1].Vendor in product_key_restrictions:
        try:
            re.match(product_key_restrictions[row[1].Vendor], initial_key)
            if re.match(product_key_restrictions[row[1].Vendor], initial_key):
                return row
        except ValueError:
            raise ValueError("RegEx mismatch")
    else:
        return row


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


