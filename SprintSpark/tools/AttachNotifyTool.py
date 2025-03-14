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
            ticket_key: str,
            receiver_email: str,
            subject: str,
            message: str,
            file_path: str = "../summary_reports/report.md",
    ):
        self.ticket_key = ticket_key
        self.receiver_email = receiver_email
        self.subject = subject
        self.message = message
        self.file_path = file_path

    def attach_and_notify(self):
        """Uploads the attachment and sends an email only if successful"""
        if self.post_issue_attachment():
            return self.send_email()
        else:
            return "Attachment upload failed. Email not sent."

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
