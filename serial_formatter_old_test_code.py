# cut from serial_formatter.py

# basic JSON and CSV to test input functions:

# writing to csv directly from serial_formatter.py was deprecated to write from database from sam_records_csv_reports.py
# with open("sam_records.csv", "w", newline='') as sr_csv:
#     headers = ["Software Vendor", "s/n", "Product Key"]
#     csv_writer = csv.DictWriter(sr_csv, fieldnames=headers)
#     csv_writer.writeheader()
#     i = 0
#     for vendor in software_vendors:
#         csv_writer.writerow({
#             "Software Vendor": software_vendors[i],
#             "s/n": serials[i],
#             "Product Key": pk_in[i]})
#         i += 1

# writing to JSON directly from serial_formatter.py was deprecated to write from database from sam_records_json_reports.py
# json_dict = ({
#         "Software Vendor": software_vendors,
#         "s/n": serials,
#         "Product Key": pk_in
#     })
# sr_json = open("D:\GitHub\serial-number-format-validator\sam_records.json", "w", encoding="utf-8")
# json.dump(json_dict, sr_json, ensure_ascii = False, indent=4, separators=(',', ': '))
# sr_json.close()

