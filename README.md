# latex-image-path-extractor
Python program to extract image paths from LaTeX documents by parsing \includegraphics-command 
# LaTeX Image Path Extractor

## Overview

The **LaTeX Image Path Extractor** is a Python script
designed to analyze LaTeX documents and extract all file names referenced by ```\includegraphics``` within the document.
This tool is intended to help users manage and verify image assets in their LaTeX projects
to remove unused files that sometimes pile up when working (LaTeX) documents.


## Features

- Extracts paths to image files from LaTeX documents using the `\includegraphics` command.
- Supports both absolute and relative paths.
- Handles optional arguments in the `\includegraphics` command.
- Compares the extracted image paths from the LaTeX document with the actual files in a specified directory.

## Future Plans


- **File Management**:
Allow users to identify and mark image files for deletion that are not referenced in the LaTeX document.

- **Graphical User Interface**:
  For more convenient usage.

## Usage

1. **Extract Image Paths**
Run the script to extract image paths (```path/to/file```)
used by ```\includegraphics[options]{path/to/file}``` from a LaTeX document (provided by passed path).
2. **Compare Files**:
Use the follow-up comparison feature to identify unused image files
by providing a path to a directory where all the images included in the LaTeX document are stored.<br>
The program compares all files in the provided path recursively to the found includings of the document
and shows the differences.
3. **Future Feature: Delete Unused Files**:
Mark files from the comparison that are not used by ```\includegraphics``` in the LaTeX document for deletion.

## Limitations
- The program only parses paths used by ```\includegraphics```-command
- Image paths of out-commented ```\includegraphics```-commands count as included
- All file types are shown by the comparison-feature, i.e. not only image files like
```eps```, ```pdf```, ```jpeg```, ```png```, etc. (keep that in mind when deleting files!).
- Program only tested under Linux

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/M5M8S10/latex-image-path-extractor
   cd latex-image-path-extractor
2. Run the script and follow instructions:
   ```bash
   python main.py

## License

This project is licensed under the [MIT License](LICENSE).
