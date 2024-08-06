import os
from project_utils import extract_image_paths, list_files_recursive


def print_header(text: str):
    """print header: prints parameter 'text' and underlines it with dashes."""
    print('\n' + text, '\n' + '-'*len(text))


# get path from user
while True:  # loops until user input is valid
    path_latex_doc = input("\nPath to tex file: ")
    path_latex_doc = os.path.normpath(path_latex_doc)  # platform independent TODO: test if needed
    # make relative paths absolute:
    if not os.path.isabs(path_latex_doc):  # is relative path?
        path_latex_doc = os.path.abspath(path_latex_doc)

    # NOTE: works with file name (if in current dir), relative and absolute paths
    # error handling:
    if not os.path.exists(path_latex_doc):  # existence
        print("No such path.")
    elif not (os.path.splitext(path_latex_doc)[1] == ".tex"):  # file type
        print("No tex file.")
    else:
        break  # user input is an existing tex file

# extract image paths
# ALTERNATIVE: maybe it is better to list every image reference (also duplicates) with line number (dictionary) and
#  filter out duplicates/current-path_latex_doc-notation only when user wants to remove unreferenced images
#  in a given directory (user input).
paths_to_images = extract_image_paths(path_latex_doc)

# make unix-like path notation from LaTeX-doc system conform
paths_to_images = [os.path.normpath(path) for path in paths_to_images]

# output found image-paths
print_header(f"Found {len(paths_to_images)} '\\includegraphics' "
             f"in LaTeX document '{os.path.basename(path_latex_doc)}':")
[print(path_to_image) for path_to_image in paths_to_images]

# get path to directory where images of LaTeX document are stored:
while True:  # loops until user input is valid
    path_to_image_dir = input("\nPath to image directory: ")
    path_to_image_dir = os.path.normpath(path_to_image_dir)  # platform independent TODO: test if needed
    # make relative paths absolute:
    if not os.path.isabs(path_to_image_dir):  # is relative path?
        path_to_image_dir = os.path.abspath(path_to_image_dir)

    # NOTE: works with  relative and absolute paths
    # error handling:
    if not os.path.exists(path_to_image_dir):  # existence
        print("No such path.")
    elif not os.path.isdir(path_to_image_dir):
        print("No directory.")
    else:
        break  # user input is an existing directory

# get list of files in given directory (supposedly image directory):
files = list_files_recursive(path_to_image_dir)

print_header(f"Found {len(files)} file(s) in directory '{path_to_image_dir}':")
[print(file) for file in files]

# make paths to images used in the LaTeX-document absolute, if relative
# (assuming images referenced in LaTeX are in a subdirectory within the directory of the LaTeX document)
# TODO: take into account when relative file paths go up a directory, e.g. '../..'
# TODO: take into account the optional '\graphicspath{ {./path/to/images/} }-LaTeX-command
for idx in range(len(paths_to_images)):
    if not os.path.isabs(paths_to_images[idx]):  # is relative path
        absolute_path = os.path.join(os.path.dirname(path_latex_doc), paths_to_images[idx])
        # check if making paths in LaTeX document absolute is plausible
        if os.path.exists(absolute_path):
            paths_to_images[idx] = absolute_path
        else:
            # TODO: proper error handling
            RED = "\033[31m"
            RESET = "\033[0m"
            TEXT = f"Conversion to absolute paths failed for reference '{paths_to_images[idx]}'"
            print(f"{RED}{TEXT}{RESET}")

# Compare list of image paths to list of files in given directory (supposedly image dir):
files_not_referenced = list()
for file in files:  # generate list of not referenced files:
    if file not in paths_to_images:
        files_not_referenced.append(file)

# print list of not referenced files:
print_header(f"List of {len(files_not_referenced)} of {len(files)} file(s) within "
             f"'{os.path.basename(path_to_image_dir)}'-directory "
             f"are not referenced in the LaTeX-document '{os.path.basename(path_latex_doc)}':")
[print(file) for file in files_not_referenced]
