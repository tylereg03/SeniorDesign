import subprocess
import os
from datetime import datetime

def collect_authors_and_dates(file_list):
    author_date_dict = {}
    
    for file_path in file_list:
        # Use git log to get author and date information for each file
        command = f"git log --format='%an %ad' -- {file_path}"
        result = subprocess.check_output(command, shell=True, text=True)

        # Process git log output
        lines = result.strip().split('\n')
        for line in lines:
            author, date_str = line.split(' ', 1)
            date = datetime.strptime(date_str, '%a %b %d %H:%M:%S %Y %z')
            
            # Store data in a dictionary
            if file_path not in author_date_dict:
                author_date_dict[file_path] = []
            author_date_dict[file_path].append({'author': author, 'date': date})
    
    return author_date_dict

# List of source files (output from CollectFiles.py)
source_files = ['file1.py', 'file2.py', 'file3.py']

# Collect authors and dates
authors_dates = collect_authors_and_dates(source_files)

# Print the collected data (you might want to save it to a file or database)
for file_path, touches in authors_dates.items():
    print(f"File: {file_path}")
    for touch in touches:
        print(f"  Author: {touch['author']}, Date: {touch['date']}")
