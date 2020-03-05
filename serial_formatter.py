import json
import re
import csv
import sqlite3
from sqlite3 import Error

'''This project will attempt to do the following:
    1) Write user-input RegEx to json file via API (browser?)
        - what format(s) do Snipe-IT and GLPI use for data storage?
        - should this RegEx library be viewable/shareable between users? should there be separate files for admins and clients?
        - 
    2) Accept user-input serial numbers via API; display warning if format doesn't match stored RegEx value for that Vendor
        - Do Snip-IT and GLPI do this already?
    3) Store user data in secure, pass-protected location (csv or sql?)
        - Again, what format(s) do Snipe-IT and GLPI use for data storage?
    4) Place size/time limits on data storage because this is a demo only

'''

#  RegEx search strings for certain software companies
auto_ex = re.compile(r'\b(\d{3}-\d{8}\b)')
auto_key = re.compile(r'([a-zA-Z]|\d)\d([a-zA-Z]|\d)[a-zA-Z]\d')
abalo_ex = re.compile(r'(\b(\d{4}-){5}\d{4}\b)')

# Select from software company: Antidex, Abalobadiah, or None (input prompt for testing,
# TODO: as drop-down menu in browser)

def entering_func(inputly):
    '''While loop with user and pre-determined exits as a decorator function'''
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

software_vendors = []

@entering_func
def soft_vend_enter():
    global software_vendors
    vend_name = input("Enter one of the following two vendors: Antidex, Abalobadiah, or None: ")
    vend_amount = int(input(f"How many licenses do you have for {vend_name}? "))
    for amnt in range(vend_amount):
        software_vendors.append(vend_name)

print(software_vendors)

# initialize list of same length as no. of software vendors entered
serials = [None for x in range(len(software_vendors))]
i = 0  # starting index to replace values in lists

@entering_func
def sn_enter():
    global serials
    global i
    global max_entries
    if i < len(serials):
        serials[i] = (input(f"Enter a serial number for {software_vendors[i]}: "))
        # if Antidex or Abalobadiah, s/n must match regex
        if software_vendors[i] == 'Antidex':
            while not re.match(auto_ex, serials[i]):
                serials[i] = (input(f"That is not a valid serial number for Antidex: "))
        if software_vendors[i] == 'Abalobadiah':
            while not re.match(abalo_ex, serials[i]):
                serials[i] = (input(f"That is not a valid serial number for Abalobadiah: "))
        i += 1

print(serials)

pk_in = [None for x in range(len(software_vendors))]
i = 0

@entering_func
def pk_enter():
    global pk_in
    global i
    if i < len(pk_in):
        pk_in[i] = (input(f"Enter a product key for {software_vendors[i]}, s/n: {serials[i]}: "))
        if software_vendors[i] == 'Antidex':
            while not re.match(auto_key, pk_in[i]):
                pk_in[i] = (input(f"That is not a valid product key for Antidex: "))
        i += 1

print(pk_in)

# # write to csv
# TODO: make separate .py file, write csv from db
# with open("sam_records.csv", "w", newline='') as sr_csv:
#     headers = ["Software Vendor", "s/n", "Product Key"]
#     csv_writer = csv.DictWriter(sr_csv, fieldnames=headers)
#     csv_writer.writeheader()
#     i = 0
#     for vendor in software_vendors:
#         csv_writer.writerow({
#             "Software Vendor": software_vendors[i],
#             "s/n": serials[i],
#             "Product Key": pk_in[i]})
#         i += 1

# # write to JSON
# TODO: make separate .py file, write JSON from db
# json_dict = ({
#         "Software Vendor": software_vendors,
#         "s/n": serials,
#         "Product Key": pk_in
#     })
# print(json_dict)
# sr_json = open("D:\GitHub\serial-number-format-validator\sam_records.json", "w", encoding="utf-8")
# json.dump(json_dict, sr_json, ensure_ascii = False, indent=4, separators=(',', ': '))
# sr_json.close()

# write to sqlite3 db
# created sam_records.db and tables for each vendor
# conn = sqlite3.connect("sam_records.db")
# c = conn.cursor()
# c.execute('''CREATE TABLE IF NOT EXISTS Antidex (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);''')
# c.execute('''CREATE TABLE IF NOT EXISTS Abalobadiah (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);''')
# c.execute('''CREATE TABLE IF NOT EXISTS None (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);''')
# conn.commit()
# conn.close()

# prepare separate lists of tuples for separate database tables
all_licenses = list(zip(software_vendors, serials, pk_in))
anti_licenses = [license[1:3] for license in all_licenses if license[0] == 'Antidex']
abalo_licenses = [license[1:3] for license in all_licenses if license[0] == 'Abalobadiah']
none_licenses = [license[1:3] for license in all_licenses if (license[0] != 'Antidex' and license[0] != 'Abalobadiah')]
print('all: ', all_licenses)
print('anti: ', anti_licenses)
print('abalo: ', abalo_licenses)
print('none: ', none_licenses)


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


def create_table(conn, create_table_sql):
    c = conn.cursor()
    try:
        c.execute(create_table_sql)
        conn.commit()
        print("table success(?)")
    except Error as e:
        print("create table error", e)
    finally:
        return c, conn


def main():
    database = "sam_records.db"
    # make table for each vendor entered as create_table_sql
    sql_create_antidex_table = "CREATE TABLE IF NOT EXISTS Antidex (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);"

    sql_create_abalobadiah_table = "CREATE TABLE IF NOT EXISTS Abalobadiah (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);"

    sql_create_none_table = "CREATE TABLE IF NOT EXISTS None (id serial PRIMARY KEY, s_n TEXT, [Product Key] TEXT);"

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_antidex_table)
        create_table(conn, sql_create_abalobadiah_table)
        create_table(conn, sql_create_none_table)
    else:
        print("Error creating database connection.")

    c = conn.cursor()

    # TODO: auto-increment id: PRIMARY KEY
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

if __name__ == '__main__':
    main()

