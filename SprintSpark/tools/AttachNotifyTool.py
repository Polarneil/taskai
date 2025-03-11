import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv
import smtplib
from email.message import EmailMessage

load_dotenv()


def attach_and_notify(ticket_key: str, receiver_email: str, subject: str, message: str, file_path: str = "./summary_reports/report.md",):
    """Uploads the attachment and sends an email only if successful"""
    if post_issue_attachment(ticket_key, file_path):
        return send_email(receiver_email, subject, message, file_path)
    else:
        return "Attachment upload failed. Email not sent."


def post_issue_attachment(ticket_key: str, file_path: str = "./summary_reports/report.md"):
    """Attaches a file to a Jira issue and returns True if successful, otherwise False"""
    try:
        jira_api_key = os.getenv('JIRA_API_KEY')
        jira_email = os.getenv('JIRA_EMAIL')
        jira_url = os.getenv('JIRA_URL')

        url = f"{jira_url}/rest/api/3/issue/{ticket_key}/attachments"
        auth = HTTPBasicAuth(username=jira_email, password=jira_api_key)

        headers = {"X-Atlassian-Token": "no-check"}

        with open(file_path, 'rb') as file:
            files = {'file': (os.path.basename(file_path), file)}
            response = requests.post(url=url, auth=auth, headers=headers, files=files)

        response.raise_for_status()
        return True
    except FileNotFoundError:
        print(f"Error: File not found at {file_path}")
    except requests.exceptions.RequestException as e:
        print(f"Request error: {e}")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    return False


def send_email(receiver_email: str, subject: str, message: str, file_path: str = None) -> str:
    """Sends an email notification with an optional file attachment"""
    try:
        gmail_app_password = os.getenv("GMAIL_APP_PASSWORD")
        sender_email = os.getenv("GMAIL_SENDER_EMAIL")

        # Create the email message
        email_message = EmailMessage()
        email_message["Subject"] = subject
        email_message["From"] = sender_email
        email_message["To"] = receiver_email
        email_message.set_content(message)

        # Attach the file if file_path is provided
        if file_path:
            try:
                with open(file_path, "rb") as file:
                    file_data = file.read()
                    file_name = os.path.basename(file_path)
                email_message.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)
            except Exception as file_error:
                return f"Error attaching file: {file_error}"

        # Send the email
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, gmail_app_password)
            server.send_message(email_message)

        return f"Email sent to {receiver_email}"
    except Exception as e:
        return f"Error sending email to {receiver_email}: {e}"
