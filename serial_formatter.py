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

result_1 = (re.findall(auto_ex, auto_test))
result_2 = (re.search(auto_ex, auto_test))
result_3 = (re.match(auto_ex, auto_test))
result_4 = (re.fullmatch(auto_ex, auto_test))

print(result_1, '\n', result_2, '\n', result_3, '\n', result_4)

# Select from software company: Antidex, Abalobadiah, or None (input prompt for testing,
# TODO: as drop-down menu in browser)

'''While loop with user and pre-determined exits as a decorator function'''
def entering_func(inputly):
    done = "No"
    max_entries = 13
    while done.upper()[0] != "Y":
        inputly()
        max_entries -= 1
        if max_entries <= 0:
            print("I can't take anymore!")
            done = 'Y'
        # elif local index is out of range, exit loop
        else:
            done = input("Are you done making entries (y/n)? ")

software_vendors = []

@entering_func
def soft_vend_enter():
    global software_vendors
    software_vendors.append(input("Enter one of the following two vendors: Antidex, Abalobadiah, or None: "))

print(software_vendors)

# initialize list of same length as no. of software vendors entered
serials = [None for x in range(len(software_vendors))]
i = 0  # starting index to replace values in lists

@entering_func
def sn_enter():
    global serials
    global i
    j = len(serials)
    if i < j:
        serials[i] = (input("Enter a serial number: "))
        i += 1
    # else:
    #     return 'stop'
print(serials)

# if Antidex or Abalobadiah, s/n must match regex
pk_in = [None for x in range(len(software_vendors))]
i = 0

@entering_func
def pk_enter():
    global pk_in
    global i
    j = len(pk_in)
    if i < j:
        pk_in[i] = (input("Enter a product key: "))
        i += 1

print(pk_in)
    # input("Enter your Product Key: ")
# if Antidex, also take user input of Prod. Key, must match regex
# if None, no format checks
# write to csv
with open("sam_records.csv", "w") as sr:
    headers = ["Software Vendor", "s/n", "Product Key"]
    csv_writer = csv.DictWriter(sr, fieldnames=headers)
    csv_writer.writeheader()
    i = 0
    for vendor in software_vendors:
        csv_writer.writerow({
            "Software Vendor": software_vendors[i],
            "s/n": serials[i],
            "Product Key": pk_in[i]})
        i += 1