import re
import os
from typing import List


# document parsing related:
def extract_image_paths(
        latex_file_path: str,
        ignore_current_path_in_pattern: bool = True,
        ignore_duplicates: bool = True
) -> List[str]:
    """
    :param latex_file_path: path/to/file.tex
    :param ignore_current_path_in_pattern: excludes optional './'-notation at the beginning of image paths in output.
    :param ignore_duplicates: only lists path once, in case of multiple references to the same image path.
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

    # remove 'current folder'-notation, since it is optional in LaTeX (NOTE: do this before removing duplicates)
    if ignore_current_path_in_pattern:
        image_paths = [path.lstrip("./") for path in image_paths]
    # remove duplicates paths
    if ignore_duplicates:
        image_paths = list(set(image_paths))
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
