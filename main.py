# import os

# def dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet, depth=0, file=None):
#     if file is None:
#         # Open the output text file with utf-8 encoding at the beginning of the recursion
#         file = open(output_txt_file, 'w', encoding='utf-8')

#     # Sort items to have consistent tree structure
#     items = sorted(os.listdir(folder_path))

#     # Iterate over all items in the current directory
#     for index, item in enumerate(items):
#         item_path = os.path.join(folder_path, item)

#         # Determine the correct tree symbol based on position
#         is_last_item = (index == len(items) - 1)
#         connector = '└── ' if is_last_item else '├── '
#         indent = '│   ' * depth + connector

#         if os.path.isdir(item_path):
#             # Write the folder name to the output text file
#             file.write(f"{indent}{item}/\n")
#             # Recursive call for the directory's contents
#             dfs_traverse_and_process_ftl_files_with_tree(item_path, output_txt_file, search_snippet, depth + 1, file)
#         elif item.endswith('.ftl'):
#             # Write the file name with a checkbox to the output text file
#             file.write(f"{indent}[ ] {item}\n")

#             # Try to open the file and search for the snippet
#             try:
#                 with open(item_path, 'r', encoding='utf-8', errors='replace') as ftl_file:
#                     for line in ftl_file:
#                         # Check if the search snippet is in the line
#                         if search_snippet in line and ('<!--' in line or '<#--' in line):
#                             print(f"Found in {item}: {line.strip()}")
#                             break
#             except UnicodeDecodeError as e:
#                 print(f"Skipping file {item_path} due to encoding error: {e}")

#     # Close the output file only if it's the original call
#     if depth == 0:
#         file.close()
#         print(f"Tree structure with .ftl files and checkboxes has been written to {output_txt_file}")

# # Usage example
# folder_path = 'C:/devenv/Git_Projects/dev'
# output_txt_file = 'ftl_tree_structure_with_checkboxes.txt2'
# search_snippet = '<!--'

# dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet)
import os

def contains_ftl_files(folder_path):
    """Check if the directory or any subdirectory contains .ftl files."""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ftl'):
                return True
    return False

def dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet, depth=0, file=None):
    if file is None:
        # Open the output text file with utf-8 encoding at the beginning of the recursion
        file = open(output_txt_file, 'w', encoding='utf-8')

    # Sort items to have consistent tree structure
    items = sorted(os.listdir(folder_path))

    # Iterate over all items in the current directory
    for index, item in enumerate(items):
        item_path = os.path.join(folder_path, item)

        # Determine the correct tree symbol based on position
        is_last_item = (index == len(items) - 1)
        connector = '└── ' if is_last_item else '├── '
        indent = '│   ' * depth + connector

        if os.path.isdir(item_path):
            # Check if the directory contains any .ftl files or subdirectories with .ftl files
            if contains_ftl_files(item_path):
                # Write the folder name to the output text file
                file.write(f"{indent}{item}/\n")
                # Recursive call for the directory's contents
                dfs_traverse_and_process_ftl_files_with_tree(item_path, output_txt_file, search_snippet, depth + 1, file)
        elif item.endswith('.ftl'):
            # Write the file name with a checkbox to the output text file
            file.write(f"{indent}[ ] {item}\n")

            # Try to open the file and search for the snippet
            try:
                with open(item_path, 'r', encoding='utf-8', errors='replace') as ftl_file:
                    for line in ftl_file:
                        # Check if the search snippet is in the line
                        if search_snippet in line and ('<!--' in line or '<#--' in line):
                            print(f"Found in {item}: {line.strip()}")
                            break
            except UnicodeDecodeError as e:
                print(f"Skipping file {item_path} due to encoding error: {e}")

    # Close the output file only if it's the original call
    if depth == 0:
        file.close()
        print(f"Tree structure with .ftl files and checkboxes has been written to {output_txt_file}")

# Usage example
folder_path = 'C:/devenv/Git_Projects/dev'
output_txt_file = 'ftl_tree_structure_with_checkboxes3.txt'
search_snippet = '<!--'

dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet)
