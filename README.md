Mad Gear Translation Tool

A simple web application that we use in Mad Gear Games to translate Android strings.xml to other languages.

Configuration notes:
- Change the global values in the configuration section of scripts.js and traductor.py
- Look out files and folders permisions, traductor.py needs to read and write files in the WORKINGPATH.
- Change LimitRequestLine to an higher value (default 8190) in your apache server if you get an error 404 (we are using 80000).

Tested on Apache 2.2.22, Linux Mint 15, Ubuntu 12.04, Firefox 25 and Chrome 31.
