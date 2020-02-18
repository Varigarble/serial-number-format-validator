import csv
import sqlite3
from sqlite3 import Error

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

conn = create_connection("sam_records.db")
c = conn.cursor()

def all_tables_report():
    global c
    c.execute("SELECT NAME from sqlite_master where type=='table'")
    all_tables = c.fetchall()
    return all_tables


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

for name in all_tables_report():
    print(name)