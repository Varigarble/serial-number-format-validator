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
c.execute("SELECT NAME from sqlite_master where type=='table'")
all_tables = c.fetchall()


def all_vendors_report():
    global all_tables
    with open("sam_vendors.csv", "w", newline='') as sr_csv:
        csv_writer = csv.writer(sr_csv)
        for vendor in all_tables:
            csv_writer.writerow(vendor)


all_vendors_report()


def all_records_report():
    global all_tables

    with open("sam_records.csv", "w", newline='') as sr_csv:
        headers = ["Software Vendor", "s/n", "Product Key"]
        csv_writer = csv.DictWriter(sr_csv, fieldnames=headers)
        csv_writer.writeheader()
        i = 1
        for table in all_tables[1:]:

            curr_table = all_tables[i][0]

            all_data = "SELECT * FROM " + curr_table

            curr_table_data = []

            for x in c.execute(all_data):
                for y in x:
                    curr_table_data.append(y)

            i2 = 0
            for _ in c.execute(all_data):
                csv_writer.writerow({
                    "Software Vendor": table[0],
                    "s/n": curr_table_data[i2 + 1],
                    "Product Key": curr_table_data[i2 + 2]
                })
                i2 += 3
            i += 1


all_records_report()

conn.close()
