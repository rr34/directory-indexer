# Usage
`main.py` is now a CLI entrypoint. Run `python main.py --help` to see the available commands.

## Index a Drive
Write a file index CSV and log file into the target directory:

```bash
python main.py index-drive /path/to/directory
```

Optional flags:

```bash
python main.py index-drive /path/to/directory --index-name custom-index.csv --log-name custom-log.txt --quiet
```

This walks the directory tree, creates an index CSV in the top-level folder, and writes a log file with timing and counts.

## Fix Dates
Normalize CSV files in a working directory by converting the `date` column to ISO format in a new `date2` column:

```bash
python main.py format-dates ./working
```

Optional flags:

```bash
python main.py format-dates ./working --output-prefix "normalized - " --quiet
```

Many banking sites export transaction CSVs with inconsistent date formats. This command finds the `date` column and writes a new CSV for each source file.

## Library Usage
If you still want to import the functions directly, these remain available:

```python
import main

main.index_drive("/path/to/directory")
main.date_formatter("/path/to/working")
```
