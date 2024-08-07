import re
import os
from typing import List


# document parsing related:
def extract_image_paths(
        latex_file_path: str,
) -> List[str]:
    """
    :param latex_file_path: path/to/file.tex
    :return: list of paths to images used as reference for 'includegraphics{...}' in given LaTeX-document.
    """

    # create regexp pattern object to extract curly bracket text in '\includegraphics[...]{...}' commands
    includegraphics_pattern = re.compile(r'\\includegraphics(?:\[.*?\])?\{(.+?)\}')  # for efficiency compile regexp obj

    image_paths: List[str] = []  # init list

    # open and read latex document:
    with open(latex_file_path, 'r') as file:
        latex_content = file.read()

        # search for '\includegraphics' command and extract paths to images
        image_paths = includegraphics_pattern.findall(latex_content)

    return image_paths


# file browsing related:
def list_files_recursive(directory: str) -> List[str] | None:
    # Create a list to store all file paths
    all_files = []

    # Walk through the directory and subdirectories
    for dirpath, _, filenames in os.walk(directory):
        for filename in filenames:
            # Construct the full file path and add it to the list
            file_path = os.path.join(dirpath, filename)
            all_files.append(file_path)

    return all_files
