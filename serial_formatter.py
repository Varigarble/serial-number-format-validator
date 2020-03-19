"""Enter SAM data into a SQLite database. There are restrictions on the data that can be entered for example fictional
vendors"""
import re
import sqlite3
from sqlite3 import Error

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
    global max_entries  # unused?
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
    sql_create_antidex_table = "CREATE TABLE IF NOT EXISTS Antidex (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"

    sql_create_abalobadiah_table = "CREATE TABLE IF NOT EXISTS Abalobadiah (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"

    sql_create_none_table = "CREATE TABLE IF NOT EXISTS None (id INTEGER PRIMARY KEY AUTOINCREMENT, s_n TEXT, [Product Key] TEXT);"

    conn = create_connection(database)

    if conn is not None:
        create_table(conn, sql_create_antidex_table)
        create_table(conn, sql_create_abalobadiah_table)
        create_table(conn, sql_create_none_table)
    else:
        print("Error creating database connection.")

    c = conn.cursor()

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
