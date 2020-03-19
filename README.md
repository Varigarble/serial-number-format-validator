# Asset Management data entry format checker

#### What is it?

This is an example Software Asset Management (SAM) database tool that uses regular expressions in Python to prevent incorrect data from being entered into a SQLite database.
It prompts a user to input vendor licensing information. 
After entering a vendor name, the associated serial numbers and product keys must match a format that that vendor uses encoded in regex.
Python scripts read from the database and output reports in JSON and CSV formats.

#### What is it not?

It does not determine if a serial number is real/authorized/valid/authentic; it only examines the format.

#### How is it used?

Start at serial_formatter.py, the input section. 
When run, you'll get prompts to enter different kinds of data, and you'll probably get stuck on what you need to enter unless you can decode the regex strings, or just copy and paste from the sample output files which are in sqlite3, json, and csv formats.
serial_formatter.py will write the input to a database file.
sam_records_json_reports.py and sam_records_csv_reports.py run queries on the database.

#### Why should it be used?

Malformed audit data is a common source of confusion and wasted time in the audit analysis process.
Bad data can be introduced in many different ways (typos, poor packaging scans, incomplete copy/paste), and it's good to catch it before it ever enters the SAM system.

#### Why shouldn't it be used?

It's incomplete - and always will be. 
It's not possible to write regexes for every product code for every product line for every vendor. 
But, for a SAM administrator or team that's familiar with regular expressions and their vendors' catalogs, this approach may be feasible.
This code is not (currently) intended to be a complete SAM system, but it offers ideas that can be tailored to fit the needs of an organization that decides to implement them.

