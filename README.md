# Usage
I prefer to run Python from a file, so I keep an untracked file called 'scripts.py' that looks like this:
```
import os
import main

working_dir = os.path.join(os.getcwd(), 'working')

# Index a Drive
# drive_to_index = r'D:/'
# main.index_drive(drive_to_index)

# Correct Dates in CSV Files
main.date_formatter(working_dir)
```

# Index Drive
Function `index_drive` indexes a drive to a `csv` file and puts the csv file in the top-level of the directory indexed for fast searching.

# Fix Dates
Many (or maybe all) banking sites have the option to download your transactions in csv. However, the date formats are often all over the place. This finds the column labeled date in the file and adjusts the date to ISO format.