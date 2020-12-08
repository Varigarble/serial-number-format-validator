import csv
import sqlite3
import subprocess
from dotenv import load_dotenv
from os import getenv

load_dotenv()
db = getenv('db_filepath')
folder = getenv('folder')


def create_connection(db_file):
    connect = None
    try:
        connect = sqlite3.connect(db_file)
        print("connect success")
        return connect
    except sqlite3.Error as e:
        print("connect failure", e)
    finally:
        return connect


def all_vendors_report():
    all_vendors_table = create_connection(db).cursor().execute("SELECT * FROM Vendors;").fetchall()
    header = ['id', 'Vendor', 'Serial Number', 'Product Key']
    all_vendors_row = [list(v) for v in all_vendors_table]
    with open(f"{folder}sam_vendors.csv", "w", newline='') as sr_csv:
        csv_writer = csv.writer(sr_csv, delimiter=' ')
        csv_writer.writerow(header)
        csv_writer.writerows(all_vendors_row)
    subprocess.Popen([f"{folder}sam_vendors.csv"], shell=True)


def one_vendor_report(vendor):
    report_title = f"{vendor}.csv"
    vendor_table = create_connection(db).cursor().execute("SELECT * FROM Vendors WHERE Vendor = ?;", (vendor,))
    header = ['id', 'Vendor', 'Serial Number', 'Product Key']
    vendor_rows = [list(row) for row in vendor_table]
    with open(f"{folder}{report_title}", "w", newline='') as v_csv:
        csv_writer = csv.writer(v_csv, delimiter=' ')
        csv_writer.writerow(header)
        csv_writer.writerows(vendor_rows)
    subprocess.Popen([f"{folder}{report_title}"], shell=True)
