# _LaTeX Image Cleaner_

## Overview

The _LaTeX Image Cleaner_ is a Python script designed to help clean the image assets folder of a LaTeX project.
It achieves this by analyzing the LaTeX document, extracting all file names referenced by `\includegraphics`,
and comparing them to the contents of the specified "assets" folder.

This tool assists users in managing and verifying image assets in their LaTeX projects,
helping to remove unused files that often accumulate during document creation.

## Features

**Image Asset Detection:**

- Scans your LaTeX document to identify and list all images referenced with `\includegraphics`.
- Recursively lists all files in the specified image assets directory.

**Unused File Identification (Diff):**

- Compares the images referenced in your LaTeX document with those in the assets directory to identify files that are not in use.*

**File Management Options:**

- Allows you to locate or delete unused image files directly from the command line, helping to keep your project organized.

**Cross-Platform Path Compatibility:**

- Accepts both Windows and Unix-like paths, enabling path copying independent of the operating system, making it easy to work across different platforms.
- Supports both absolute and relative paths, providing flexibility in how you organize and access your files.

## Usage

1. **Run the python script**

   Run the script via
   ````bash
   python main.py
   ````
   > Requires [Python](https://www.python.org/downloads/) to be installed
2. **Specify the path of the _LaTeX_ document**:
    
   Specify the path of the _LaTeX_ document by typing or copy and pasting the path, e.g.
   ````bash
   Path to tex file: latex/doc.tex
   ````
   > The program lists files paths used by ```\includegraphics[options]{path/to/file.ext}```.
3. **Specify the path of directory for the image asset**:
 
   Specify the path of directory used as image asset by typing or copy and pasting the path, e.g.
   ````bash
   Path Path to image directory: latex/images
   ````

   > The program lists files paths found in the specified directory **recursively**,<br>
   > followed up by a list of files not referenced
   > by ```\includegraphics[options]{path/to/file.ext}``` _LaTeX_-command (_diff_).

4. **Locate or Delete Unused Files (OPTIONAL)**:

      1. **Select Operation to Locate or Delete Unused Files**:

         Select operation _LOCATE_ or _DELETE_ to locate or delete unused files via

         - **l** (LOCATE)
         - **d** (DELETE)
         ```
         List of 3 of 8 file(s) within 'images'-directory are not referenced in the LaTeX-document 'doc.tex': 
         0: [IGNORE] C:\...\latex\images\image1.jpeg
         1: [IGNORE] C:\...\latex\images\image2.pdf
         2: [IGNORE] C:\...\latex\images\subfolder\image1.jpeg

         *** Commands ***
         l: Mark files to open location in file manager
         d: Mark files for deletion
         q: Quit application
         What now> d
         ```

   2. **Mark Unused Files from the List to be Located or Deleted**:
   
       Select all or individual files by number via
       - **a** (all)
       - **\<number in shown range>** (individual; can be done repeatedly)
       ```
       0: [IGNORE] C:\...\latex\images\image1.jpeg
       1: [IGNORE] C:\...\latex\images\image2.pdf
       2: [IGNORE] C:\...\latex\images\subfolder\image1.jpeg
   
       *** Commands ***
       0-2: Select file by number
       a: Select all files
       l: Locate marked file(s)
       c: Cancel operation (marks all files as IGNORE)
       q: Quit application
       DELETE>> 1
      ```
   3. **Submit or Cancel Selection**:
   
      Depending on the previous selected operation (localizing or deleting),
      submit your selection or cancel operation via
      - **l** (submits locate)
      - **d** (submits delete)
      - **c** (cancels operation)
      ```
      0: [IGNORE] C:\...\latex\images\image1.jpeg
      1: [DELETE] C:\...\latex\images\image2.pdf
      2: [IGNORE] C:\...\latex\images\subfolder\image1.jpeg

      *** Commands ***
      0-2: Select file by number
      a: Select all files
      d: Delete marked file(s)
      c: Cancel operation (marks all files as IGNORE)
      q: Quit application
      DELETE>> d
      ```
      
      >⚠️ **WARNING**<br>
      Read [Disclaimer](#-disclaimer) and [Limitations](#limitations) before use.

5. **Quit Program**:

   The program now restarts from _operation selection_.
   Quit program via **q** (Quit)
   ```
   List of 2 of 8 file(s) within 'images'-directory are not referenced in the LaTeX-document 'doc.tex': 
   0: [IGNORE] C:\...\latex\images\image1.jpeg
   1: [IGNORE] C:\...\latex\images\subfolder\image1.jpeg

   *** Commands ***
   l: Mark files to open location in file manager
   d: Mark files for deletion
   q: Quit application
   What now> q
   ```

## Limitations
- Only parses paths used by `\includegraphics`.
- Does not work with multiline `\includegraphics` commands (may cause false positives).
- Does not work if a default directory for image assets is defined, i.e., `\graphicspath{{path/to/your/images/}{another/path/to/images/}}` (may cause false positives).
- Image paths in commented-out `\includegraphics` commands count as included.
- The comparison feature lists all file types, not just image files like `eps`, `pdf`, `jpeg`, `png`, etc. (keep this in mind when deleting files).

## ⚠️ Disclaimer

### Caution When Using the Delete Feature
**Files marked as `DELETE` will be permanently deleted on submission.**<br>
This action **cannot be undone**, and the deleted files **cannot be restored or retrieved**.<br>
Please ensure you have selected the correct files before submitting deletion.

It is recommended that you first create a backup copy of the data.

The maintainers of this repository hold **no liability** for any lost data. Use this feature at your own risk.

## Future Plans

- **Graphical User Interface**:
  For more convenient usage.

- **Command-Line Arguments**:
  Enable the use of arguments for specifying paths and operations at execution, allowing for automated cleanup via scripts (e.g., batch scripts). 

## Installation

1. Clone this repository:

   ```bash
   git clone https://github.com/M5M8S10/latex-image-cleaner
2. Navigate to project directory:
   ```bash
   cd latex-image-cleaner
3. Run the script and follow instructions in the command line interface (see [Usage](#usage)):
   ```bash
   python main.py

## License

This project is licensed under the [MIT License](LICENSE).
