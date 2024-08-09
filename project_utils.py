import re
import os
from typing import List, Dict
import platform
import subprocess


def print_header(text: str):
    """print header: prints parameter 'text' and underlines it with dashes."""
    print('\n' + text, '\n' + '-'*len(text))


def text_bold(text: str) -> str:
    TEXT_BLD = "\033[1m"  # ANSI escape code for bold text
    TEXT_RST = "\033[0m"  # ANSI escape code to reset text color
    return f"{TEXT_BLD}{text}{TEXT_RST}"


def text_yellow(text: str) -> str:
    """colors string yellow"""
    TEXT_YEL = "\033[33m"  # ANSI escape code for yellow text
    TEXT_RST = "\033[0m"  # ANSI escape code to reset text color
    return f"{TEXT_YEL}{text}{TEXT_RST}"


def text_initial_yellow(text: str) -> str:
    """colors the first letter of the string yellow"""
    TEXT_YEL = "\033[33m"  # ANSI escape code for yellow text
    TEXT_RST = "\033[0m"  # ANSI escape code to reset text color
    return f"{TEXT_YEL}{text[0]}{TEXT_RST}{text[1:]}"


def text_red(text: str) -> str:
    """colors string red"""
    TEXT_RED = "\033[31m"  # ANSI escape code for yellow text
    TEXT_RST = "\033[0m"  # ANSI escape code to reset text color
    return f"{TEXT_RED}{text}{TEXT_RST}"


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
            os.remove(file_path)  # cross-platform command
            print(f"File '{file_path}' has been removed.")
        else:
            print(f"File '{file_path}' does not exist.")
    except Exception as e:
        print(f"An error occurred while trying to remove the file: {e}")


# right adjusted print:
def print_operation_info(operation_infos: List[Dict]) -> None:
    """prints dictionary with 'index', 'marking' and 'path' keys in tabular, formatted form."""
    # calculate  max width of 'index' to vertically align entries:
    max_width = max(len(str(item['index'])) for item in operation_infos)
    # print via list comprehension
    [
        print(
            f"{str(item['index']).rjust(max_width)}: "  # index right adjusted
            f"[{item['marking']}] "  # marking in square brackets
            f"{item['path']}"  # path as is
        ) for item in operation_infos]


# module tests
if __name__ == '__main__':
    remove_file("invalid/path/that/does/certainly/not/exists/on/my/or/any/other/machine")
