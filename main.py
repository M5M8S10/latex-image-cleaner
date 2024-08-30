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
import argparse


parser = argparse.ArgumentParser(
    description="Shows and/or deletes unused image files of a LaTeX document.")
parser.add_argument(
    '--doc',
    metavar='path/to/file.tex',
    help="Path to the LaTeX document")
parser.add_argument(
    '--dir',
    metavar='path/to/directory',
    help="Path to the image directory")
parser.add_argument(
    '--diff',
    action='store_true',  # acts as True/False if this flag is used/not used
    help="Lists the files of the specified folder that are not used in the specified document")
parser.add_argument(
    '--delete',
    action='store_true',  # acts as True/False if this flag is used/not used
    help="Deletes the files of the specified folder that are not used in the specified document")
parser.add_argument(
    '--verbose', '-v',
    action='store_true',  # acts as True/False if this flag is used/not used
    help='Lists found references in LaTeX document and files within image directory')
args = parser.parse_args()

# get path to LaTeX document from user or parse from argument
while True:  # loops until user input is valid
    if args.doc:  # argument provided?
        path_latex_doc = args.doc
        args.doc = None  # clear argument to not assign from it again (in possible next iteration)
    else:
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
files_in_doc = extract_referenced_files(path_latex_doc)

# make path notation from LaTeX-doc (unix-like) platform dependant, to fit with user inputs
# (also removes 'current folder'-notation, i.e. "./" ; optional in LaTeX documents):
files_in_doc = [os.path.normpath(path) for path in files_in_doc]
# remove duplicates:
files_in_doc = list(set(files_in_doc))  # do this after normalizing of paths

# output found image-paths
if args.verbose:
    print_header(f"Found {len(files_in_doc)} '\\includegraphics' "
                 f"in LaTeX document '{os.path.basename(path_latex_doc)}':")
    [print(path_to_image) for path_to_image in files_in_doc]

# get path to image directory from user or parse from argument
while True:  # loops until user input is valid
    if args.dir:  # argument provided?
        path_to_image_dir = args.dir
        args.dir = None  # clear argument to not assign from it again (in possible next iteration)
    else:
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
files_in_dir = list_files_recursive(path_to_image_dir)

if args.verbose:
    print_header(f"Found {len(files_in_dir)} file(s) in directory '{path_to_image_dir}':")
    [print(file) for file in files_in_dir]

# make referenced image paths in the LaTeX-document absolute
# (assuming images referenced in LaTeX are in a subdirectory within the directory of the LaTeX document):
# TODO: take into account when relative file paths go up a directory, e.g. '../..'
# TODO: take into account the optional '\graphicspath{ {./path/to/images/} }-LaTeX-command
for idx in range(len(files_in_doc)):
    if not os.path.isabs(files_in_doc[idx]):  # is relative path
        absolute_path = os.path.join(os.path.dirname(path_latex_doc), files_in_doc[idx])
        # check if making paths in LaTeX document absolute is plausible
        if os.path.exists(absolute_path):
            files_in_doc[idx] = absolute_path
        else:
            # TODO: proper error handling
            print(text_red(f"Conversion to absolute paths failed for reference '{files_in_doc[idx]}'"))

if args.diff or args.delete:
    files_not_referenced = [file for file in files_in_dir if file not in files_in_doc]
    if len(files_not_referenced) == 0:
        print(f"No unreferenced files found in '{os.path.basename(path_to_image_dir)}'-directory.")
        quit()
    if args.diff:
        print(f"{len(files_not_referenced)} of {len(files_in_dir)} file(s)"
              f" within '{os.path.basename(path_to_image_dir)}'-directory not reverenced:")
        [print(file) for file in files_not_referenced]
    if args.delete:
        print("Deleting unreferenced files...", end=" ")  # TODO: count and show number of deleted files
        [remove_file(file) for file in files_not_referenced]
        print(f"Done")
    # after performing argument-based operations do not proceed to interactive operation and quit the program
    quit()

# Marking user marking
while True:  # loops until quit

    # refresh list of files (in case files have been deleted; see below)
    files_in_dir = list_files_recursive(path_to_image_dir)
    # generate list of not referenced files
    # (diff of files in given - supposedly image - dir and found paths in document):
    files_not_referenced = [file for file in files_in_dir if file not in files_in_doc]

    # print list of not referenced files:
    print_header(f"List of {len(files_not_referenced)} of {len(files_in_dir)} file(s) within "
                 f"'{os.path.basename(path_to_image_dir)}'-directory "
                 f"are not referenced in the LaTeX-document '{os.path.basename(path_latex_doc)}':")

    # For better handling of markings (user input), convert diff-result into a list of dictionaries:
    files_not_referenced = [
        dict(
            index=idx,
            marking="IGNORE",
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
        print(f"{text_initial_yellow('c')}: {text_initial_yellow('Cancel')} operation (marks all files as IGNORE)")
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
            elif user_input == "l":  # confirm operation 'locate'
                # open all as 'LOCATE' marked files:
                [open_in_file_browser(file["path"]) for file in files_not_referenced if file["marking"] == "LOCATE"]
                exit_selection = True  # go back to operation selection ("What now"-input loop)
                break
            elif user_input == "d":  # confirm operation 'delete'
                # delete all as 'DELETE' marked files:
                [remove_file(file["path"]) for file in files_not_referenced if file["marking"] == "DELETE"]
                exit_selection = True  # go back to operation selection ("What now"-input loop)
                break
            elif user_input == "c":  # cancel (mark all file 'IGNORE')
                # NOTE: 'IGNORE' is default marking and done when refreshing list at "What now"-input loop
                exit_selection = True  # go back to operation selection ("What now"-input loop)
                break
            elif user_input == "q":  # quit application
                quit()
