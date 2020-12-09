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
    table_list_dict = [{"id": f"{row[0]}",
                        "Vendor": f"{row[1]}",
                        "Serial Number": f"{row[2]}",
                        "Product Key": f"{row[3]}"}
                       for row in table]
    table_reformatted = {}
    for row in table_list_dict:
        table_reformatted[row["Vendor"]] = {}
    for row in table_list_dict:
        table_reformatted[row["Vendor"]][row["id"]] = {'Serial Number': row['Serial Number'], 'Product Key':
            row['Product Key']}
    json_dict = {"Software Vendors": table_reformatted}
    av_json = open(f"{folder}sam_vendors.json", "w", encoding="utf-8")
    json.dump(json_dict, av_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    av_json.close()
    subprocess.Popen([f"{folder}sam_vendors.json"], shell=True)


def one_vendor_report(vendor):
    table = create_connection(db).cursor().execute("SELECT * FROM Vendors WHERE Vendor = ?;", (vendor,))
    table_list_dict = [{"id": f"{row[0]}",
                        "Serial Number": f"{row[2]}",
                        "Product Key": f"{row[3]}"}
                       for row in table]
    table_reformatted = {str(vendor): {}}
    for row in table_list_dict:
        table_reformatted[str(vendor)][row["id"]] = {'Serial Number': row['Serial Number'], 'Product Key':
                          row['Product Key']}
    json_dict = table_reformatted
    sv_json = open(f"{folder}{vendor}.json", "w", encoding="utf-8")
    json.dump(json_dict, sv_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    sv_json.close()
    subprocess.Popen([f"{folder}{vendor}.json"], shell=True)
