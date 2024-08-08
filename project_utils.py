import re
import os
from typing import List
import platform
import subprocess


# document parsing related:
def extract_referenced_files(
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


def open_in_file_browser(path: str):
    """Opens path in file browser. file browser is platform dependant."""
    if platform.system() == 'Windows':
        subprocess.run(['explorer', os.path.normpath(path)])
    elif platform.system() == 'Darwin':
        subprocess.run(['open', path])
    elif platform.system() == 'Linux':
        subprocess.run(['xdg-open', path])
    else:
        raise OSError("Unsupported operating system")


def remove_file(file_path: str) -> None:
    """
    Removes the specified file if it exists.

    :param file_path: The path to the file to be removed.
    """
    try:
        # Check if the file exists
        if os.path.isfile(file_path):
            # Remove the file
            os.remove(file_path)    # cross-platform command
            print(f"File '{file_path}' has been removed.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to remove the file: {e}")


# module tests
if __name__ == '__main__':
    remove_file("invalid/path/that/does/certainly/not/exists/on/my/or/any/other/machine")
