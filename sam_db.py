import sqlite3
from sqlite3 import Error
from collections import namedtuple  # query tuples as named?

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

sql_create_vendor_table = 'CREATE TABLE IF NOT EXISTS Vendors (id INTEGER PRIMARY KEY AUTOINCREMENT, Vendor TEXT, \
                            Serial_Number TEXT, Product_Key TEXT);'
sql_add_vendor = 'INSERT INTO Vendors (Vendor) VALUES (?);'
sql_update_sn = 'UPDATE Vendors SET Serial_Number = ? WHERE id = ?;'
sql_update_vendor = 'UPDATE Vendors SET Vendor = ? WHERE Vendor = ?;'
sql_update_product_key = 'UPDATE Vendors SET Product_Key = ? WHERE id = ?;'


def update_vendor(new, old):
    print(new, old)
    with conn:
        c = conn.cursor()
        c.execute(sql_update_vendor, (new, old))
        conn.commit()


def serial_one_row_updater(sn_set_out):
    c = conn.cursor()
    for row in sn_set_out:
        c.execute(sql_update_sn, (row.Serial_Number, row.id))
    conn.commit()


def product_key_row_updater(pk_set_out):
    c = conn.cursor()
    for row in pk_set_out:
        c.execute(sql_update_product_key, (row.Product_Key, row.id))
    conn.commit()


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


def view_vendors():
    with conn:
        vend_list = list(conn.cursor().execute("SELECT DISTINCT Vendor FROM Vendors ORDER BY Vendor"))
    return [vendor_tuple[0] for vendor_tuple in vend_list]


def view_sns():
    with conn:
        sn_list = list(conn.cursor().execute("SELECT DISTINCT Vendor, Serial_Number FROM Vendors ORDER BY Vendor"))
    return sn_list


def view_all():
    with conn:
        all_list = list(conn.cursor().execute("SELECT id, Vendor, Serial_Number, Product_Key FROM Vendors ORDER BY Vendor"))
    return all_list


#  namedtuple testing:
def view_all_namedtuple():
    Row = namedtuple('Row', 'id, Vendor, Serial_Number, Product_Key')
    i = 0
    rows_dict = {}
    for _ in view_all():
        k = 'row' + str(view_all()[i][0])
        row = Row(*view_all()[i])
        rows_dict[k] = row
        i += 1
    return rows_dict


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

def view_all_dict():
    pass


def soft_vend_enter(vend_name, amount):
    with conn:
        for amnt in range(amount):
            conn.execute("INSERT INTO Vendors (Vendor) VALUES (?);", (vend_name,))
    print(f"{amount} license(s) of {vend_name} added to database.")


def sn_write(sn_add_list):
    print(f"preparing to write {sn_add_list}")
    with conn:
        for entry in sn_add_list:
            conn.execute("INSERT INTO Vendors (Vendor, Serial_Number) VALUES (?, ?);", entry)


def update_table():
    pass





# if __name__ == '__main__':
#     main()