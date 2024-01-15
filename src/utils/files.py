import os


def search_files_recursively(directory:str, extension:str) -> list:
    found_files = []

    for foldername, _, filenames in os.walk(directory):
        for filename in filenames:
            if filename.endswith(extension):
                found_files.append(os.path.join(foldername, filename))

    return found_files
