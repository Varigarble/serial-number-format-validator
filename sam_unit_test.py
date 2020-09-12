import unittest
import sqlite3
import string
import json
import re

invalid_char = re.compile(r'.*\\+.*')

conn = sqlite3.connect(":memory:")
c = conn.cursor()

c.execute("CREATE TABLE IF NOT EXISTS test (id INTEGER PRIMARY KEY AUTOINCREMENT, test_text TEXT);")
conn.commit()
c.execute("SELECT NAME from sqlite_master where type=='table'")

text1 = "NSN\\1"  # r"\": SyntaxError: EOL while scanning string literal
text2 = "\""
text3 = "\\\\\\"  # r"\\\": SyntaxError: EOL while scanning string literal

if re.match(invalid_char, text1):
    print("text1 contains an invalid character")
    text1_res = ""
    for ch in text1:
        if ch != "\\":
            text1_res += ch
        else:
            text1_res += "/"
        text1 = text1_res
    print("resolved: ", text1)
if re.match(invalid_char, text2):
    print("text2 contains an invalid character")
if re.match(invalid_char, text3):
    print("text3 contains an invalid character")

insert = "INSERT INTO test (test_text) VALUES (?);"
c.execute(insert, (text1,))
c.execute(insert, (text2,))
c.execute(insert, (text3,))
conn.commit()

c.execute("SELECT * FROM test")
table_data = c.fetchall()
# conn.commit()
print(table_data)

all_none = {}

for row in table_data:
    print(row[0])
    print(row[1])
    # str_text = r"{}".format(row[1])
    all_none[row[0]] = row[1]
    # print(row, "cooked: ", row[1], "raw: ", str_text)
print("all_none = ", all_none)
json_dict = ({"None:": all_none})
noner_json = open("C:\\Users\Ghuleh\Documents\GitHub\serial-number-format-validator\\test_none_records.json", "w",
                  encoding="utf-8")
json.dump(json_dict, noner_json, ensure_ascii=False, indent=4, separators=(',', ': '))
noner_json.close()

#
# id_cond = ("NULL",)
# c.execute("SELECT * FROM test WHERE NOT id=?", id_cond)
#
# for elem in table:
#     print(table)

# ellist = []
# for elem in c:
#     ellist.append()
# print(len(ellist))

# class MyTestCase(unittest.TestCase):
#     def test_something(self):
#         self.assertEqual(True, False)
#
#
# if __name__ == '__main__':
#     unittest.main()
#
