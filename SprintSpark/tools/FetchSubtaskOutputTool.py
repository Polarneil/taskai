import os
from crewai.tools import tool


@tool("FetchSubtaskOutputTool")
def get_text_files(directory_path: str = "../outputs") -> dict:
    """
    Retrieves a dictionary of .txt files in a given directory with file names as keys and file contents as values.
    """
    try:
        text_files = {}
        for f in os.listdir(directory_path):
            file_path = os.path.join(directory_path, f)
            if os.path.isfile(file_path) and f.lower().endswith('.txt'):
                with open(file_path, 'r', encoding='utf-8') as file:
                    text_files[f] = file.read()
        return text_files

    except FileNotFoundError:
        return {"Error": f"Directory '{directory_path}' not found."}
    except NotADirectoryError:
        return {"Error": f"'{directory_path}' is not a directory."}
    except PermissionError:
        return {"Error": f"Permission denied for directory '{directory_path}'."}
    except Exception as e:
        return {"Error": f"An unexpected error occurred: {e}"}
