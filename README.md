# Asset Management data entry format checker with gui

#### What it is:

This is an example Software Asset Management (SAM) database with a gui that can prevent incorrect data from being entered. 
Database reports can be produced in JSON and CSV formats and automatically open.

#### How it's used:

First, set the database filepath and name, and the folder where you want reports saved, in the .env file. Next, run 
sam_gui.py, the input section. If starting with an empty database, the only option that will work is "Add Software Vendor."
serial_formatter.py is configured to enforce correctly formatted serial number entries for the fictional companies 
Abalobadiah and OAuthDex, and correctly formatted product key entries for OAuthDex. The example database contains sample
data matching the RegEx restrictions for these companies.

#### Why it should be used:

Malformed audit data is a common source of confusion and wasted time in the audit analysis process.
Bad data can be introduced in many different ways (typos, poor packaging scans, incomplete copy/paste), and it's good 
to catch it before it ever enters the SAM system.

#### Why it shouldn't be used:

It's incomplete - and always will be. 
It's not possible to write regular expressions for every product code for every product line for every vendor that's 
ever existed or will exist. But, for a SAM administrator or team that's familiar with regular expressions and their 
vendors' catalogs, this approach may be feasible. This project is not (currently) a complete SAM system, but it offers 
ideas that can be tailored to fit the needs of an organization that decides to implement them.