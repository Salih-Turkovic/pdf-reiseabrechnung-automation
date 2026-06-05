# PDF Travel Expense Automation

## Problem
The accounting team had to manually open each PDF, read the travel date,
travel code, and expense report number, rename the document accordingly,
and create the target folder if it didn't exist yet.

Total backlog: 3,104 documents × ~3 minutes = approximately 155 hours
of manual work.

## Solution
Python script that processes PDF travel expense reports automatically:
- Extracts travel date, travel code, and report number from each PDF
- Renames every document in a standardized format
- Automatically creates missing year and month folders
- Moves documents into the correct folder structure (year/month)
- PDFs that cannot be processed are moved to a separate error folder
  with a CSV error log — no data loss

## Result
155 hours of manual accounting work eliminated.
3,104 documents processed in minutes instead of weeks.

## Usage
```bash
python rename_pdfs.py \
  --input /path/to/input \
  --output /path/to/output \
  --fehler /path/to/errors
```

## Technologies
- Python 3
- pdfplumber — extract text from PDFs
- tqdm — progress bar
- pathlib, shutil, csv, re — standard libraries

## Note
File names and paths are anonymized. No original documents included.[requirements.txt.rtf](https://github.com/user-attachments/files/28628025/requirements.txt.rtf)
[umbenennen.py](https://github.com/user-attachments/files/28627611/umbenennen.py)
