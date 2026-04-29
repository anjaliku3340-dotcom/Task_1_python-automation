import os
from datetime import datetime

LOG_FILE = "operations.log"

FILE_CATEGORIES = {
    "images": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg"],
    "documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt", ".xls", ".xlsx", ".ppt", ".pptx"],
    "videos": [".mp4", ".avi", ".mov", ".mkv", ".flv", ".wmv"],
    "audio": [".mp3", ".wav", ".aac", ".flac", ".ogg"],
    "archives": [".zip", ".tar", ".gz", ".rar", ".7z"],
}

UNWANTED_EXTENSIONS = [".tmp", ".log", ".bak", ".old", ".aux"]


def log_action(action, message, success=True):
    """Write a log entry with timestamp, action, and result."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    status = "SUCCESS" if success else "ERROR"
    entry = f"{timestamp} | {action} | {status} | {message}\n"

    try:
        with open(LOG_FILE, "a", encoding="utf-8") as log_file:
            log_file.write(entry)
    except Exception as error:
        print(f"Could not write to log file: {error}")


def validate_directory(path):
    """Return the normalized absolute path if valid, otherwise None."""
    if not path:
        print("No directory path provided.")
        return None

    normalized = os.path.abspath(path)

    if not os.path.isdir(normalized):
        print(f"Directory does not exist: {normalized}")
        return None

    return normalized


def get_files(directory):
    """Return a list of files in the given directory (non-recursive)."""
    try:
        return [f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))]
    except Exception as error:
        print(f"Could not list files in directory: {error}")
        log_action("List files", f"Could not list files in {directory}: {error}", success=False)
        return []


def rename_files(directory):
    """Rename files in bulk with prefix, suffix, or numbering."""
    files = get_files(directory)
    if not files:
        print("No files found to rename.")
        return

    prefix = input("Enter prefix to add (leave blank for none): ").strip()
    suffix = input("Enter suffix to add before extension (leave blank for none): ").strip()
    numbering_choice = input("Add numbering? (y/n): ").strip().lower() == "y"
    start_number = 1

    if numbering_choice:
        try:
            start_number = int(input("Enter starting number: ").strip())
        except ValueError:
            start_number = 1
            print("Invalid number entered. Using 1.")

    print(f"Renaming {len(files)} files in {directory}...")

    for index, filename in enumerate(sorted(files), start=start_number):
        name, extension = os.path.splitext(filename)
        new_name = f"{prefix}{name}{suffix}{extension}"
        if numbering_choice:
            new_name = f"{prefix}{index}{suffix}{extension}"

        original_path = os.path.join(directory, filename)
        new_path = os.path.join(directory, new_name)

        try:
            os.rename(original_path, new_path)
            print(f"Renamed: {filename} -> {new_name}")
            log_action("Rename file", f"{filename} -> {new_name}")
        except Exception as error:
            print(f"Failed to rename {filename}: {error}")
            log_action("Rename file", f"Failed to rename {filename}: {error}", success=False)


def sort_files_by_type(directory):
    """Sort files into folders based on known file type categories."""
    files = get_files(directory)
    if not files:
        print("No files found to sort.")
        return

    print("Sorting files into folders by type...")
    for filename in files:
        _, extension = os.path.splitext(filename)
        extension = extension.lower()
        matched_category = None

        for category, extensions in FILE_CATEGORIES.items():
            if extension in extensions:
                matched_category = category
                break

        if matched_category is None:
            matched_category = "others"

        target_folder = os.path.join(directory, matched_category)
        target_path = os.path.join(target_folder, filename)

        try:
            if not os.path.exists(target_folder):
                os.makedirs(target_folder)
            os.rename(os.path.join(directory, filename), target_path)
            print(f"Moved: {filename} -> {matched_category}{os.sep}")
            log_action("Sort file", f"Moved {filename} to {matched_category}")
        except Exception as error:
            print(f"Failed to move {filename}: {error}")
            log_action("Sort file", f"Failed to move {filename}: {error}", success=False)


def delete_unwanted_files(directory):
    """Delete files based on unwanted extensions or custom extension input."""
    files = get_files(directory)
    if not files:
        print("No files found to delete.")
        return

    display_extensions = ", ".join(UNWANTED_EXTENSIONS)
    print(f"Default unwanted extensions: {display_extensions}")
    custom_input = input("Enter additional extensions to delete (comma-separated, e.g. .tmp, .cache), or leave blank: ").strip()
    custom_extensions = [ext.strip().lower() for ext in custom_input.split(",") if ext.strip()]

    extensions_to_delete = set(UNWANTED_EXTENSIONS + custom_extensions)
    deleted_any = False

    for filename in files:
        _, extension = os.path.splitext(filename)
        if extension.lower() in extensions_to_delete:
            file_path = os.path.join(directory, filename)
            try:
                os.remove(file_path)
                print(f"Deleted: {filename}")
                log_action("Delete file", f"Deleted {filename}")
                deleted_any = True
            except Exception as error:
                print(f"Failed to delete {filename}: {error}")
                log_action("Delete file", f"Failed to delete {filename}: {error}", success=False)

    if not deleted_any:
        print("No unwanted files were found for deletion.")


def display_menu():
    """Print the user operation menu."""
    print("\nFile Management Automation")
    print("1. Rename files in bulk")
    print("2. Sort files into folders by type")
    print("3. Delete unwanted files")
    print("4. Exit")


def main():
    """Main entry point for the script."""
    print("Welcome to the File Manager Automation Script.")

    directory_path = input("Enter the directory path to manage: ").strip()
    directory = validate_directory(directory_path)
    if not directory:
        return

    while True:
        display_menu()
        choice = input("Choose an operation (1-4): ").strip()

        if choice == "1":
            rename_files(directory)
        elif choice == "2":
            sort_files_by_type(directory)
        elif choice == "3":
            delete_unwanted_files(directory)
        elif choice == "4":
            print("Exiting. Goodbye.")
            break
        else:
            print("Invalid choice. Please enter a number between 1 and 4.")


if __name__ == "__main__":
    main()
