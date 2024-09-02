import os

# Global dictionary to store the user's decisions for specific lines
decision_memory = {}

def contains_ftl_files(folder_path):
    """Check if the directory or any subdirectory contains .ftl files."""
    for root, dirs, files in os.walk(folder_path):
        for file in files:
            if file.endswith('.ftl'):
                return True
    return False

def process_comment(line):
    """Process the comment according to the rules specified."""
    # Skip comments with $HTMLId
    if '<!-- $HTMLId:' in line:
        return line, False

    modified = False
    # Handle ${} conversion
    if '${' in line:
        if '<!--' in line and '-->' in line:
            line = line.replace('<!--', '<#--').replace('-->', '-->')
            modified = True

    return line, modified

def user_interaction(line, file_name):
    """Interact with the user to decide whether to Convert, Delete, or Ignore."""
    if line in decision_memory:
        # Apply the remembered decision
        action = decision_memory[line]
        if action == 'C':
            line, modified = process_comment(line)
            return line, modified, False
        elif action == 'D':
            return '', False, True
        elif action == 'I':
            return line, False, False
    else:
        # If no decision was remembered, ask the user
        while True:
            print(f"\nLine to be processed: {line.strip()}")
            try:
                choice = input("Type 'C' to Convert, 'D' to Delete, 'I' to Ignore: ").strip().upper()

                if choice in ('C', 'D', 'I'):
                    decision_memory[line] = choice  # Remember the decision
                    if choice == 'C':
                        line, modified = process_comment(line)
                        return line, modified, False
                    elif choice == 'D':
                        with open('deleted_log.txt', 'a', encoding='utf-8') as log_file:
                            log_file.write(f"Deleted from {file_name}: {line.strip()}\n")
                        return '', False, True
                    elif choice == 'I':
                        return line, False, False
                else:
                    raise ValueError("Invalid input. Please type 'C', 'D', or 'I'.")
            except ValueError as e:
                print(e)

def dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet, change_log_file, depth=0, file=None):
    if file is None:
        file = open(output_txt_file, 'w', encoding='utf-8')

    items = sorted(os.listdir(folder_path))

    for index, item in enumerate(items):
        item_path = os.path.join(folder_path, item)

        is_last_item = (index == len(items) - 1)
        connector = '└── ' if is_last_item else '├── '
        indent = '│   ' * depth + connector

        if os.path.isdir(item_path):
            if contains_ftl_files(item_path):
                file.write(f"{indent}{item}/\n")
                dfs_traverse_and_process_ftl_files_with_tree(item_path, output_txt_file, search_snippet, change_log_file, depth + 1, file)
        elif item.endswith('.ftl'):
            file.write(f"{indent}[ ] {item}\n")
            changes_made = False

            try:
                with open(item_path, 'r', encoding='utf-8', errors='replace') as ftl_file:
                    lines = ftl_file.readlines()

                with open(item_path, 'w', encoding='utf-8') as ftl_file:
                    for line in lines:
                        if 'IF YOU COME ACROSS THIS LINE,' in line or '<!-- end of Step Progress Indicator table -->' in line:
                            with open('deleted_log.txt', 'a', encoding='utf-8') as log_file:
                                log_file.write(f"Automatically deleted from {item_path}: {line.strip()}\n")
                            continue

                        if '<!-- $HTMLId:' in line:
                            ftl_file.write(line)
                            continue

                        if '${' in line and '<!--' in line and '-->' in line:
                            line, modified, to_delete = user_interaction(line, item)

                            if to_delete:
                                continue

                            if modified:
                                changes_made = True

                        elif '<!-- removeAccount=${removeAccount?string} -->' in line:
                            line, modified = process_comment(line)
                            changes_made = True

                        elif '</th><!--${colspan}-->' in line:
                            ftl_file.write(line)
                            continue

                        else:
                            ftl_file.write(line)

            except UnicodeDecodeError as e:
                print(f"Skipping file {item_path} due to encoding error: {e}")

            if changes_made:
                with open(change_log_file, 'a', encoding='utf-8') as log_file:
                    log_file.write(f"Changes made in {item_path}\n")

    if depth == 0:
        file.close()
        print(f"Tree structure with .ftl files and checkboxes has been written to {output_txt_file}")

# Usage example
folder_path = 'C:/devenv/Git_Projects/dev'
output_txt_file = 'ftl_tree_structure_with_checkboxesv4.txt'
change_log_file = 'ftl_change_logv4.txt'
search_snippet = '<!--'

dfs_traverse_and_process_ftl_files_with_tree(folder_path, output_txt_file, search_snippet, change_log_file)
