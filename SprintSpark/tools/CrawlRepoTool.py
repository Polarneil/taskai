import git
import os
import shutil
from dotenv import load_dotenv
from crewai.tools import tool

load_dotenv()

git_repo_url = os.getenv("REPO_URL")


@tool("CrawlRepoTool")
def crawl_repo_to_dict(repo_url=git_repo_url, clone_path="../cloned_repos/") -> dict:
    """
    Clones a Git repository and stores file contents in a dictionary.

    Args:
        repo_url (str): The URL of the Git repository.
        clone_path (str): The path to clone the repository to.

    Returns:
        dict: A dictionary containing file paths as keys and file contents as values,
              or None if an error occurs.
    """
    try:
        os.makedirs(clone_path, exist_ok=True)  # check the directory exists
        repo = git.Repo.clone_from(repo_url, clone_path)

        repo_contents = {}

        for item in repo.tree().traverse():
            if item.type == 'blob':
                try:
                    content = item.data_stream.read().decode('utf-8', errors='ignore')
                    repo_contents[item.path] = content
                except UnicodeDecodeError:
                    print(f"Warning: Could not decode file {item.path}. Skipping.")
                except Exception as e:
                    print(f"Warning: Error reading file {item.path}: {e}")

        return repo_contents

    except git.exc.GitCommandError as e:
        return {"message": f"Error: Git command - {e}"}
    except Exception as e:
        return {"message": f"An unexpected error occurred: {e}"}
    finally:  # ensure cleanup.
        if os.path.exists(clone_path):
            shutil.rmtree(clone_path)  # shutil.rmtree for directory removal
