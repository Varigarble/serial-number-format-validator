import re

#  RegEx search strings for certain software vendors
oauth_sn = re.compile(r'\b(\d{3}-\d{8}\b)')
oauth_key = re.compile(r'\b([a-zA-Z]|\d)\d([a-zA-Z]|\d)[a-zA-Z]\d\b')
abalo_sn = re.compile(r'(\b(\d{4}-){5}\d{4}\b)')

serial_number_restrictions = {'OAuthDex': oauth_sn, 'Abalobadiah': abalo_sn}
product_key_restrictions = {'OAuthDex': oauth_key}


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
