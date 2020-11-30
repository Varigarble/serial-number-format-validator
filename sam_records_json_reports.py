# TODO: can change paths to files to .env values

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


def antidex_report():
    c.execute("SELECT * FROM Antidex")
    all_adx = c.fetchall()
    json_dict = ({"Antidex:": all_adx})
    adxr_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\\antidex_records.json", "w",
                     encoding="utf-8") # TODO: can change path to file to .env value
    json.dump(json_dict, adxr_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    adxr_json.close()


# antidex_report()


def abalobadiah_report():
    c.execute("SELECT * FROM Abalobadiah")
    all_abl = c.fetchall()
    json_dict = ({"Abalobadiah:": all_abl})
    ablr_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\\abalobadiah_records.json", "w",
                     encoding="utf-8")
    json.dump(json_dict, ablr_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    ablr_json.close()


# abalobadiah_report()


def none_report():
    c.execute("SELECT * FROM None")
    all_none = c.fetchall()
    json_dict = ({"None:": all_none})
    noner_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\\none_records.json", "w",
                      encoding="utf-8")
    json.dump(json_dict, noner_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    noner_json.close()


# none_report()


def all_vendors_report():
    tables_reformatted = [table[0] for table in all_tables]
    json_dict = ({"Software Vendors:": tables_reformatted})
    sv_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\sam_vendors.json", "w",
                   encoding="utf-8")
    json.dump(json_dict, sv_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    sv_json.close()


# all_vendors_report()


def all_tables_report():  # old version
    global all_tables
    dicts_data = {}
    i = 1
    for table in all_tables[1:]:
        curr_table = all_tables[i][0]
        c.execute("SELECT * FROM " + curr_table)
        all_curr_data = c.fetchall()
        dicts_data[curr_table] = all_curr_data
        i += 1
    json_dict = (dicts_data)
    sr_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\sam_records_1.json", "w",
                   encoding="utf-8")
    json.dump(json_dict, sr_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    sr_json.close()


# all_tables_report()


def all_records_report():  # New 11/2020
    tables = create_connection("sam_records.db").cursor().execute("SELECT * FROM Vendors").fetchall()
        # c.execute('SELECT * FROM Vendors;')
    # TODO: use namedtuples instead of indexes?
    tables_reformatted = [(f"id: {table[0]}",
                           f"Vendor: {table[1]}",
                           f"Serial Number: {table[2]}",
                           f"Product Key: {table[3]}")
                          for table in tables]
    json_dict = ({"Software Vendors": tables_reformatted})
    sv_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\sam_vendors_1.json", "w",
                   encoding="utf-8")
    json.dump(json_dict, sv_json, ensure_ascii=False, indent=4, separators=(',', ': '))
    sv_json.close()


# all_records_report()

conn.close()
