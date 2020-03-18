# SAM data entry format checker

#### What is it?

This is an example Software Asset Management database tool that uses regular expressions in Python to prevent incorrect data from being entered into a SQLite database.
It prompts a user to input software vendor licensing information. 
After entering a software vendors' name, the associated serial numbers and product keys must match a format that that vendor uses encoded in regex.
Python scripts read from the database and output reports in JSON and CSV formats.

#### What is it not?

It does not determine if a serial number is real/authorized/valid/authentic; it only examines the format.

#### Why should one use this?

As an IP paralegal with a number of years of experience in software audit analysis, I've seen that malformed audit data is a common source of confusion and wasted time.
Bad data can be introduced in many different ways (typos, poor packaging scans, incomplete copy/paste), and it's good to catch it before it ever enters the SAM system.

#### Why shouldn't one use this?

It's incomplete - and always will be. 
It's not possible to write regexes for every product code for every product line for every manufacturer. 
But, for a SAM administrator or team that's familiar with their vendors' catalogs and regular expressions, this approach may be feasible.
This code is not (currently) intended to be a complete SAM system and would need to be tailored to fit the needs of the organization using it.
