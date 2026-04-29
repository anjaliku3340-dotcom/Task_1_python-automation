
# Task_1_python-automation

A Python-based automation script designed to simplify everyday file management tasks such as renaming, organizing, and cleaning directories. This tool helps reduce manual effort by automating repetitive operations with a simple command-line interface.

## Features

- Bulk rename files with prefix, suffix, or numbering
- Sort files into folders by type (images, documents, videos, audio, archives, others)
- Delete unwanted files based on default or custom extensions
- Cross-platform support for Windows and Linux
- Generates `operations.log` with timestamped actions and results

## Usage

1. Run the script:

```bash
python file_manager.py
```

2. Enter the directory path when prompted.
3. Choose one of the operations:
   - Rename files in bulk
   - Sort files into folders by type
   - Delete unwanted files
   - Exit

## Example

```text
Welcome to the File Manager Automation Script.
Enter the directory path to manage: C:\Users\Acer\Documents\TestFolder

File Management Automation
1. Rename files in bulk
2. Sort files into folders by type
3. Delete unwanted files
4. Exit
Choose an operation (1-4): 1
Enter prefix to add (leave blank for none): new_
Enter suffix to add before extension (leave blank for none): _v1
Add numbering? (y/n): y
Enter starting number: 1
Renaming 3 files in C:\Users\Acer\Documents\TestFolder...
Renamed: report.docx -> new_1_v1.docx
Renamed: image.png -> new_2_v1.png
Renamed: notes.txt -> new_3_v1.txt
```

## Log Output

All operations are recorded in `operations.log` with the following details:

- Time of operation
- Action performed
- Success or error message

Example log entry:

```text
2026-04-29 14:32:00 | Rename file | SUCCESS | report.docx -> new_1_v1.docx
```
