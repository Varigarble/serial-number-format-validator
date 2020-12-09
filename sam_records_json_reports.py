import json
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
    table = create_connection(db).cursor().execute("SELECT * FROM Vendors")
    table_reformatted = [(f"id: {row[0]}",
                           f"Vendor: {row[1]}",
                           f"Serial Number: {row[2]}",
                           f"Product Key: {row[3]}")
                          for row in table]
    json_dict = ({"Software Vendors": table_reformatted})
    av_json = open(f"{folder}sam_vendors.json", "w", encoding="utf-8")
    json.dump(json_dict, av_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    av_json.close()
    subprocess.Popen([f"{folder}sam_vendors.json"], shell=True)


def one_vendor_report(vendor):
    table = create_connection(db).cursor().execute("SELECT * FROM Vendors WHERE Vendor = ?;", (vendor,))
    table_reformatted = [(f"id: {row[0]}",
                           f"Vendor: {row[1]}",
                           f"Serial Number: {row[2]}",
                           f"Product Key: {row[3]}")
                          for row in table]
    json_dict = ({f"{vendor}": table_reformatted})
    sv_json = open(f"{folder}{vendor}.json", "w", encoding="utf-8")
    json.dump(json_dict, sv_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    sv_json.close()
    subprocess.Popen([f"{folder}{vendor}.json"], shell=True)
