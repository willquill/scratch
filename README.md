# scratch
For scratch projects

## pdf_metadata.sh

This script allows you to quickly and effortlessly modify the Title, Author, and Subject of an infinite number of PDF files in the current directory with a single command.

It is especially useful for modifying the metadata on PDF sheet music before importing into [forScore](https://forscore.co/). This allows you to automatically map the PDF metadata to the forScore values for Title, Composers, and Genres. The script can be modified to mass-modify, say, only the subject (genres) of a collection of PDF files, leaving the title/author as-is by simply deleting the references to title and author.

After running the script to update the files and then importing the PDF files into forScore, use the Select All function in forScore and tap "Fetch" to retrieve the metadata from the PDF files and update the Title, Author, and Subject for each imported PDF.

### Requirements

- Your computer must be able to run bash scripts, and you must have [exiftool](https://exiftool.org/install.html) installed.
- If you have macOS, install [Homebrew](https://formulae.brew.sh/formula/exiftool) and then execute `brew install exiftool` in your terminal.
- If you have Ubuntu, run `sudo apt update` followed by `sudo apt install exiftool`.

### How it works

You may have the following files in your directory:

```
pdf_metadata.sh
The Doors - Riders on the Storm.pdf
The Beatles - Yesterday.pdf
```

If you navigate to that directory in your terminal (macOS, Linux, or Windows WSL) and run `sh pdf_metadata.sh` it will do the following for each file:

1. Interpret all text before ` - ` as the Author.
2. Interpret all text after the ` - ` as the Title.
3. Use the value you assign to "subject" in the script as the Subject.
4. Modify the PDF metadata values to match the text interpreted from steps 1-3.

*Note: Don't worry - it won't add the space before or after the hyphen to your author/title!*

To see how any PDF metadata value translates to a forScore value, see [this page](https://forscore.co/developers-pdf-metadata/).

### How to run it

1. Place the `pdf_metadata.sh` file in the same directory as your PDF files
2. Modify the value of "subject" to your desired sheet music genre. The value you assign to "subject" will be intepreted in forScore as the Genre after import.
3. Execute `sh pdf_metadata.sh` in your terminal in that directory.

Because this script was written to apply the same genre for all PDF files, you should put all "Pop Rock" PDF files into a single directory with this script and run the script. Then move the script to a directory for a different genre and modify the script to change the value of "subject" to the appropriate genre before executing it again.
