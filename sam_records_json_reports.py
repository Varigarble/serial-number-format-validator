import json
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


def all_records_report():
    global tables_reformatted
    json_dict = ({
            "Software Vendor": tables_reformatted})
        #     "s/n": serials,
        #     "Product Key": pk_in
        # })
    print(json_dict)
    sr_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\sam_records.json", "w", encoding="utf-8")
    json.dump(json_dict, sr_json, ensure_ascii = False, indent=4, separators=(',', ': '))
    sr_json.close()


all_records_report()