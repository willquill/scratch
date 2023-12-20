#!/bin/bash

# forScore doc: http://forscore.co/developers-pdf-metadata/
# Loop through each PDF file in the current directory and
# replace Title and Author according to filename and
# replace Subject with "Pop Rock"
for pdf_file in *.pdf; do
    
    echo "Starting '$pdf_file'"
    
    # Extract the title and author from the filename using regex
    # The regex assumes the format: Author - Title.pdf
    # i.e. Bill Withers - Ain't No Sunshine.pdf
    title=$(echo "$pdf_file" | grep -oP '(?<= - ).*(?=.pdf)')
    author=$(echo "$pdf_file" | grep -oP '^[^-]+'| sed 's/ *$//g')
    subject="Pop Rock"
                
    # Use exiftool to set the title and author metadata
    exiftool -Title="$title" -Author="$author" -Subject="$subject" "$pdf_file"

    echo "Set title '$title' and author '$author' for $pdf_file\n"

    # Delete the original file created by exiftool
    rm "${pdf_file}_original"
done

