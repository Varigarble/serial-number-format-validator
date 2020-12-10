# Asset Management data entry format checker with gui

#### What it is:

This is an example Software Asset Management (SAM) database with a gui that can prevent incorrect data from being entered. 
Database reports can be produced in JSON and CSV formats and automatically open.

#### How it's used:

First, set the database filepath and name, and the folder where you want reports saved, in a .env file. Next, run 
sam_gui.py, the input section. If starting with an empty database, the only option that will work is "Add Software Vendor."
serial_formatter.py is configured to enforce correctly formatted serial number entries for the fictional companies 
Abalobadiah and OAuthDex, and correctly formatted product key entries for OAuthDex. The example database contains sample
data matching the RegEx restrictions for these companies.

#### Why it should be used:

Malformed audit data is a common source of confusion and wasted time in the audit analysis process.
Bad data can be introduced in many ways (typos, poor packaging scans, incomplete copy/paste), and it's good to catch it 
before it ever enters the SAM system.

#### Why it shouldn't be used:

This project is currently in a demonstration/proof-of-concept phase. There is only one database table with four columns.
A more complete SAM application might have a system of checking licenses in and out to employees.
It's also not possible to write regular expressions for every product code for every product line for every vendor that's 
ever existed or will exist. There are ideas in here, particularly some neat PySimpleGUI tricks, that can be incorporated
into other projects.

![add software vendor](https://raw.githubusercontent.com/Varigarble/serial-number-format-validator/master/1_163504.JPG?raw=True)
![add serial number](https://github.com/Varigarble/serial-number-format-validator/blob/master/2_164537.JPG)
![add product key](https://github.com/Varigarble/serial-number-format-validator/blob/master/3_171649.JPG)
![update software vendor](https://github.com/Varigarble/serial-number-format-validator/blob/master/4_165743.JPG)
![update product key](https://github.com/Varigarble/serial-number-format-validator/blob/master/6_170031.JPG)
![view vendor list](https://github.com/Varigarble/serial-number-format-validator/blob/master/7_170255.JPG)
![get reports](https://github.com/Varigarble/serial-number-format-validator/blob/master/8_163820.JPG)

#### Known issues:

- Individual vendor report file names incorporate vendor names. The file creation process may fail if there are special
characters in the vendor's name.
