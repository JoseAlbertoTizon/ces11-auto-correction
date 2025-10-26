#!/bin/bash

# Check if a folder argument was provided
if [ "$#" -ne 1 ]; then
    echo "Usage: $0 <folder>"
    exit 1
fi

DIR="$1"

# Verify directory exists
if [ ! -d "$DIR" ]; then
    echo "Error: '$DIR' is not a directory"
    exit 1
fi

# Go to the target directory
cd "$DIR" || exit 1

# Iterate over all files in the folder
for file in *; do
    [ -f "$file" ] || continue  # Skip if not a file

    # Separate filename and extension
    name="${file%.*}"
    ext="${file##*.}"

    # Transform the part before the extension:
    # capitalize every letter that follows an underscore
    new_name=$(echo "$name" | sed -E 's/_([a-z])/_\U\1/g')

    # Reattach the extension if there was one
    if [ "$name" != "$ext" ]; then
        new_file="${new_name}.${ext}"
    else
        new_file="$new_name"
    fi

    # Rename if the name changed
    if [ "$file" != "$new_file" ]; then
        mv "$file" "$new_file"
        echo "Renamed: '$file' → '$new_file'"
    fi
done
