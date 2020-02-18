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
tables_reformatted = [table[0] for table in all_tables]


def all_vendors_report():
    global all_tables
    with open("sam_vendors.csv", "w", newline='') as sr_csv:
        csv_writer = csv.writer(sr_csv)
        for vendor in all_tables:
            csv_writer.writerow(vendor)


all_vendors_report()


def all_records_report():
    global tables_reformatted
    with open("sam_records.csv", "w", newline='') as sr_csv:
        headers = ["Software Vendor", "s/n", "Product Key"]
        csv_writer = csv.DictWriter(sr_csv, fieldnames=headers)
        csv_writer.writeheader()
        i = 0
        for vendor in tables_reformatted:
            csv_writer.writerow({
                "Software Vendor": tables_reformatted[i],})
                # "s/n": serials[i],
                # "Product Key": pk_in[i]})
            i += 1


all_records_report()


conn.close()