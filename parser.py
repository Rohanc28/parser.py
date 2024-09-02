import os
from collections import deque

def bfs_traverse_and_process_ftl_files(folder_path, output_txt_file, search_snippet):
    # check if folder
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    queue = deque([folder_path])

    with open(output_txt_file, 'w') as file:
        while queue:
            current_folder = queue.popleft()

            for item in os.listdir(current_folder):
                item_path = os.path.join(current_folder, item)

                if os.path.isdir(item_path):
                    queue.append(item_path)  # Add directories to the queue
                elif item.endswith('.ftl'):
                    # Write the file name with a checkbox to the output text file
                    file.write(f"[ ] {item}\n")

                    # Try to open the file and search for the snippet
                    with open(item_path, 'r') as ftl_file:
                        for line in ftl_file:
                            # Check if the search snippet is in the line
                            if search_snippet in line and ('<!--' in line or '<#--' in line):
                                print(f"Found in {item}: {line.strip()}")
                                break

    print(f"Names of all .ftl files with checkboxes have been written to {output_txt_file}")

# Usage example
folder_path = 'C:/devenv/Git_Projects/dev'
output_txt_file = 'ftl_filenames_with_checkboxes.txt'
search_snippet = '<!--'

bfs_traverse_and_process_ftl_files(folder_path, output_txt_file, search_snippet)
"""
import os
from collections import deque

def bfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet):
    # Check if the folder exists
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Initialize BFS queue with tuple (directory_path, depth_level)
    queue = deque([(folder_path, 0)])

    # Open the output text file
    with open(output_txt_file, 'w') as file:
        # BFS traversal
        while queue:
            current_folder, depth = queue.popleft()

            # Process each item in the current folder
            for item in sorted(os.listdir(current_folder)):
                item_path = os.path.join(current_folder, item)

                # Create tree-like structure with indentation
                indent = '│   ' * depth + '├── ' if depth > 0 else ''

                if os.path.isdir(item_path):
                    queue.append((item_path, depth + 1))  # Add directories to the queue
                    file.write(f"{indent}{item}/\n")
                elif item.endswith('.ftl'):
                    # Write the file name with a checkbox to the output text file
                    file.write(f"{indent}[ ] {item}\n")

                    # Try to open the file and search for the snippet
                    with open(item_path, 'r') as ftl_file:
                        for line in ftl_file:
                            # Check if the search snippet is in the line
                            if search_snippet in line and ('<!--' in line or '<#--' in line):
                                print(f"Found in {item}: {line.strip()}")
                                break

    print(f"Tree structure with .ftl files and checkboxes has been written to {output_txt_file}")

# Usage example
folder_path = '/path/to/your/folder'
output_txt_file = 'ftl_tree_structure_with_checkboxes.txt'
search_snippet = 'your_search_snippet'

bfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet)

"""