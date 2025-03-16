import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage
import base64
import json

load_dotenv()


class UserDelivery:
    def __init__(
            self,
            github_owner: str,
            github_repo: str,
            branch_name: str,
            base_branch: str,
            repo_file_path: str,
            file_content: str,
            commit_message: str,
            github_token: str,

            ticket_key: str,
            receiver_email: str,
            subject: str,
            message: str,
            file_path: str,
    ):
        self.github_owner = github_owner
        self.github_repo = github_repo
        self.branch_name = branch_name
        self.base_branch = base_branch
        self.repo_file_path = repo_file_path
        self.file_content = file_content
        self.commit_message = commit_message
        self.github_token = github_token

        self.ticket_key = ticket_key
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message
        self.file_path = file_path

    def attach_and_notify(self):
        try:
            if not self.post_issue_attachment():
                return "Attachment upload failed."

            if not self.create_github_branch_and_file():
                return "GitHub branch and file creation failed."

            return self.send_email()
        except Exception as e:
            return f"An unexpected error occurred: {e}"

    def post_issue_attachment(self):
        """Attaches a file to a Jira issue and returns True if successful, otherwise False"""
        try:
            jira_api_key = os.getenv('JIRA_API_KEY')
            jira_email = os.getenv('JIRA_EMAIL')
            jira_url = os.getenv('JIRA_URL')

            url = f"{jira_url}/rest/api/3/issue/{self.ticket_key}/attachments"
            auth = HTTPBasicAuth(username=jira_email, password=jira_api_key)

            headers = {"X-Atlassian-Token": "no-check"}

            with open(self.file_path, 'rb') as file:
                files = {'file': (os.path.basename(self.file_path), file)}
                response = requests.post(url=url, auth=auth, headers=headers, files=files)

            response.raise_for_status()
            return True
        except FileNotFoundError:
            print(f"Error: File not found at {self.file_path}")
        except requests.exceptions.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        return False

    def send_email(self) -> str:
        """Sends an email notification with an optional file attachment"""
        try:
            gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
            sender_email = os.getenv("GMAIL_SENDER_EMAIL")

            # Create the email message
            email_message = EmailMessage()
            email_message["Subject"] = self.subject
            email_message["From"] = sender_email
            email_message["To"] = self.receiver_email
            email_message.set_content(self.message)

            # Attach the file if file_path is provided
            if self.file_path:
                try:
                    with open(self.file_path, "rb") as file:
                        file_data = file.read()
                        file_name = os.path.basename(self.file_path)
                    email_message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
                except Exception as file_error:
                    return f"Error attaching file: {file_error}"

            # Send the email
            with smtplib.SMTP("smtp.gmail.com", 587) as server:
                server.starttls()
                server.login(sender_email, gmail_app_password)
                server.send_message(email_message)

            return f"Email sent to {self.receiver_email}"
        except Exception as e:
            return f"Error sending email to {self.receiver_email}: {e}"

    def create_github_branch_and_file(self):
        """
        Creates a new branch in a GitHub repository, adds a file to it, and pushes the changes.
        Returns:
            bool: True if successful, False otherwise.
        """
        headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
        }

        try:
            # 1. Get the SHA of the base branch's latest commit
            base_branch_url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/git/refs/heads/{self.base_branch}"
            response = requests.get(base_branch_url, headers=headers)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            base_branch_sha = response.json()["object"]["sha"]

            # 2. Create the new branch
            create_branch_url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/git/refs"
            branch_data = {
                "ref": f"refs/heads/{self.branch_name}",
                "sha": base_branch_sha,
            }
            response = requests.post(create_branch_url, headers=headers, json=branch_data)
            response.raise_for_status()

            # 3. Create or update the file
            create_file_url = f"https://api.github.com/repos/{self.github_owner}/{self.github_repo}/contents/{self.repo_file_path}"
            file_data = {
                "message": self.commit_message,
                "content": base64.b64encode(self.file_content.encode()).decode(),
                "branch": self.branch_name,
            }

            response = requests.put(create_file_url, headers=headers, json=file_data)
            response.raise_for_status()
            print(response.json())

            return True

        except requests.exceptions.RequestException as e:
            print(f"Error: {e}")
            if response is not None:
                try:
                    error_details = response.json()
                    print(f"GitHub API Error Details: {json.dumps(error_details, indent=2)}")
                except json.JSONDecodeError:
                    print("Could not parse error response from Github")
            return False
        except KeyError as e:
            print(f"KeyError: {e}. Possible issue with API response structure.")
            return False
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
            return False
