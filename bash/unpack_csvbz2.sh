#!/bin/bash

# Directory to search
SEARCH_DIR="/path/to/your/directory"

# Go through every child folder and file in the directory
find "$SEARCH_DIR" -type f -name '*.csv.bz2' | while read -r file; do
    echo "Extracting: $file"
    # Extract the file
    bzip2 -d "$file"
    echo "Extraction complete, file deleted: $file"
done

echo "All files have been extracted and original .bz2 files deleted."
