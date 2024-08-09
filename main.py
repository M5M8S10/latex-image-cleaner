import os
from project_utils import extract_referenced_files
from project_utils import list_files_recursive
from project_utils import open_in_file_browser
from project_utils import remove_file
from project_utils import print_operation_info
from project_utils import print_header
from project_utils import text_bold
from project_utils import text_red
from project_utils import text_yellow
from project_utils import text_initial_yellow


# get path from user
while True:  # loops until user input is valid
    path_latex_doc = input("\nPath to tex file: ")
    path_latex_doc = os.path.normpath(path_latex_doc)  # make platform independent
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
referenced_file_paths = extract_referenced_files(path_latex_doc)

# make path notation from LaTeX-doc (unix-like) platform dependant, to fit with user inputs
# (also removes 'current folder'-notation, i.e. "./" ; optional in LaTeX documents):
referenced_file_paths = [os.path.normpath(path) for path in referenced_file_paths]
# remove duplicates:
referenced_file_paths = list(set(referenced_file_paths))  # do this after normalizing of paths

# output found image-paths
print_header(f"Found {len(referenced_file_paths)} '\\includegraphics' "
             f"in LaTeX document '{os.path.basename(path_latex_doc)}':")
[print(path_to_image) for path_to_image in referenced_file_paths]

# get path to directory where images of LaTeX document are stored:
while True:  # loops until user input is valid
    path_to_image_dir = input("\nPath to image directory: ")
    path_to_image_dir = os.path.normpath(path_to_image_dir)  # make platform independent
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

# make referenced image paths in the LaTeX-document absolute
# (assuming images referenced in LaTeX are in a subdirectory within the directory of the LaTeX document):
# TODO: take into account when relative file paths go up a directory, e.g. '../..'
# TODO: take into account the optional '\graphicspath{ {./path/to/images/} }-LaTeX-command
for idx in range(len(referenced_file_paths)):
    if not os.path.isabs(referenced_file_paths[idx]):  # is relative path
        absolute_path = os.path.join(os.path.dirname(path_latex_doc), referenced_file_paths[idx])
        # check if making paths in LaTeX document absolute is plausible
        if os.path.exists(absolute_path):
            referenced_file_paths[idx] = absolute_path
        else:
            # TODO: proper error handling
            print(text_red(f"Conversion to absolute paths failed for reference '{referenced_file_paths[idx]}'"))


# Marking user marking
while True:  # loops until quit

    # refresh list of files (in case files have been deleted; see below)
    files = list_files_recursive(path_to_image_dir)
    # generate list of not referenced files
    # (diff of files in given - supposedly image - dir and found paths in document):
    files_not_referenced = [file for file in files if file not in referenced_file_paths]

    # print list of not referenced files:
    print_header(f"List of {len(files_not_referenced)} of {len(files)} file(s) within "
                 f"'{os.path.basename(path_to_image_dir)}'-directory "
                 f"are not referenced in the LaTeX-document '{os.path.basename(path_latex_doc)}':")

    # Make dictionary of diff for markings (user input):
    files_not_referenced = [
        dict(
            index=idx,
            marking=None,
            path=files_not_referenced[idx]
        ) for idx in range(len(files_not_referenced))
    ]

    # print dict. of unreferenced files:
    print_operation_info(files_not_referenced)

    print(text_bold('\n*** Commands ***'))
    print(f"{text_initial_yellow('l')}: Mark files to open {text_initial_yellow('location')} in file manager")
    print(f"{text_initial_yellow('d')}: Mark files for {text_initial_yellow('deletion')}")
    print(f"{text_initial_yellow('q')}: {text_initial_yellow('Quit')} application")
    while True:
        match input(f"{text_bold('What now>')}"):
            case "l":
                marking = "LOCATE"
                break
            case "d":
                marking = "DELETE"
                break
            case "q":
                quit()

    exit_selection = False
    while not exit_selection:
        # print dict. of unreferenced files:
        print_operation_info(files_not_referenced)

        print(text_bold('\n*** Commands ***'))
        print(f"{text_initial_yellow('0')}-{text_yellow(f'{len(files_not_referenced)-1}')}: Select file by number")
        print(f"{text_initial_yellow('a')}: Select {text_initial_yellow('all')} files")
        print(f"{text_initial_yellow(f'{marking[0].lower()}')}: "
              f"{text_initial_yellow(f'{marking.capitalize()}')} marked file(s)")
        print(f"{text_initial_yellow('q')}: {text_initial_yellow('Quit')} application")

        while True:
            user_input = input(text_bold(f"{marking}>>"))
            if user_input.isnumeric():  # mark by number
                if int(user_input) in range(len(files_not_referenced)):
                    files_not_referenced[int(user_input)]["marking"] = marking
                    break
            elif user_input == "a":  # mark all
                for file in files_not_referenced:
                    file["marking"] = marking
                break
            elif user_input == marking[0].lower():  # confirm operation
                for file in files_not_referenced:
                    if file["marking"] == "LOCATE":
                        open_in_file_browser(os.path.dirname(file["path"]))
                    if file["marking"] == "DELETE":
                        remove_file(file["path"])
                exit_selection = True  # go back to marking ("What now"-input loop)
                break
            elif user_input == "q":  # quit application
                quit()
