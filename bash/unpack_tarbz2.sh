#!/bin/bash

# Directory to search
SEARCH_DIR="/mnt/d/eve_database/destruction_data/data.everef.net/killmails/2020"

# Go through every child folder and file in the directory
find "$SEARCH_DIR" -type f -name '*.tar.bz2' | while read -r file; do
    echo "Extracting: $file"
    # Extract the .tar.bz2 file
    tar -xjf "$file" -C "$(dirname "$file")"
    echo "Extraction complete: $file"
    # Optionally, delete the original .tar.bz2 file
    rm "$file"
    echo "Original file deleted: $file"
done

echo "All .tar.bz2 files have been extracted and original files deleted."
