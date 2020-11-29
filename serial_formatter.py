import re

#  RegEx search strings for certain software vendors
anti_ex = re.compile(r'\b(\d{3}-\d{8}\b)')
anti_key = re.compile(r'\b([a-zA-Z]|\d)\d([a-zA-Z]|\d)[a-zA-Z]\d\b')
abalo_ex = re.compile(r'(\b(\d{4}-){5}\d{4}\b)')
jj_key = re.compile(r'\b\d{3}\b')

serial_number_restrictions = {'Antidex': anti_ex, 'Abalobadiah': abalo_ex}
product_key_restrictions = {'Antidex': anti_key, 'jj': jj_key}


def sn_checker(row, initial_key):
    if row is None:
        row = ''
    if initial_key is None:
        initial_key = ''
    if row[1].Vendor in serial_number_restrictions:
        try:
            re.match(serial_number_restrictions[row[1].Vendor], initial_key)
            if re.match(serial_number_restrictions[row[1].Vendor], initial_key):
                return row
        except ValueError:
            raise ValueError("RegEx mismatch")
    else:
        return row


def pk_checker(row, initial_key):
    if row is None:
        row = ''
    if initial_key is None:
        initial_key = ''
    if row[1].Vendor in product_key_restrictions:
        try:
            re.match(product_key_restrictions[row[1].Vendor], initial_key)
            if re.match(product_key_restrictions[row[1].Vendor], initial_key):
                return row
        except ValueError:
            raise ValueError("RegEx mismatch")
    else:
        return row
