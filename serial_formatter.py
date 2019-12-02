import json
import re
import csv
import sqlite3
# conn = sqlite3.connect("name.db")
# conn.close() at end of file

'''This project will attempt to do the following:
    1) Write user-input RegEx to json file via API (browser?)
        - what format(s) do Snipe-IT and GLPI use for data storage?
        - should this RegEx library be viewable/shareable between users? should there be separate files for admins and clients?
        - 
    2) Accept user-input serial numbers via API; display warning if format doesn't match stored RegEx value for that Vendor
        - Do Snip-IT and GLPI do this already?
    3) Store user data in secure, pass-protected location (csv or sql?)
        - Again, what format(s) do Snipe-IT and GLPI use for data storage?
    4) Place size/time limits on data storage because this is a demo only

'''



auto_test = "check these: 555-12345678, 47t-87654321, 6669-69696969, 212-32342452"

auto_ex = re.compile(r'(\b(\d{3}-\d{8}\b))')

result_1 = str(auto_ex.findall(auto_test))
result_2 = str(auto_ex.search(auto_test))
result_3 = str(auto_ex.match(auto_test))
result_4 = str(auto_ex.fullmatch(auto_test))

print(result_1, '\n', result_2, '\n', result_3, '\n', result_4)

# Select from software company: Antidex, Abalobadiah, or None (input prompt for testing,
    # TODO: as drop-down menu in browser)

# try
soft_vend_in = ["Antidex", "Abalobadaiah"]
    # input("Enter one of the following two vendors: Antidex, Abalobadaiah, or None: ")
# except
# Take user input of s/n
sn_in = ["666-69696969", "1111-2222-3333-4444-5555-6666"]
    # input("Enter your serial number: ")

# if Antidex or Abalobadiah, s/n must match regex
pk_in = ["06EY5", None]
    # input("Enter your Product Key: ")
# if Antidex, also take user input of Prod. Key, must match regex
# if None, no format checks
# write to csv
with open("sam_records.csv", "w") as sr:
    headers = ["Software Vendor", "s/n", "Product Key"]
    csv_writer = csv.DictWriter(sr, fieldnames=headers)
    csv_writer.writeheader()
    i = 0
    for vendor in soft_vend_in:
        csv_writer.writerow({
            "Software Vendor": soft_vend_in[i],
            "s/n": sn_in[i],
            "Product Key": pk_in[i]})
        i += 1