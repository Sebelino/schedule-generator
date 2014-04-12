Generates an HTML page containing a weekly schedule from a CSV file.

My aim has been to make a tool that is easy to install and use, with minimal dependencies involved.

# Usage
Store your data in data.csv. Then simply run:
```
python2.7 schedgen.py > index.html
```
or, if you have make installed:
```
make
```
index.html will then contain the calendar. Note that main.css needs to reside in the same directory.
