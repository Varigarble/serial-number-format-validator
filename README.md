# SAM data entry format checker

#### What is it?

This is an example Software Asset Management database tool that uses regular expressions in Python to prevent incorrect data from being entered into a SQLite database.
It prompts a user to input software vendor licensing information. 
After entering a software vendor's name, the associated serial numbers and product keys must match a format that that vendor uses encoded in regex.
Python scripts read from the database and output reports in JSON and CSV formats.

#### What is it not?

It does not determine if a serial number is real/authorized/valid/authentic; it only examines the format.

#### How is it used?

Start at serial_formatter.py, the input section. 
When run, you'll get prompts to enter different kinds of data, and you'll probably get stuck on what you need to enter unless you can decode the regex strings, or just copy and paste from the sample output files which are in sqlite3, json, and csv formats.
serial_formatter.py will write the input to a database file.
sam_records_json_reports.py and sam_records_csv_reports.py run queries on the database.

#### Why should it be used?

As an IP paralegal with a number of years of experience in software audit analysis, I've seen that malformed audit data is a common source of confusion and wasted time.
Bad data can be introduced in many different ways (typos, poor packaging scans, incomplete copy/paste), and it's good to catch it before it ever enters the SAM system.

#### Why shouldn't it be used?

It's incomplete - and always will be. 
It's not possible to write regexes for every product code for every product line for every manufacturer. 
But, for a SAM administrator or team that's familiar with their vendors' catalogs and regular expressions, this approach may be feasible.
This code is not (currently) intended to be a complete SAM system and would need to be tailored to fit the needs of the organization using it.
