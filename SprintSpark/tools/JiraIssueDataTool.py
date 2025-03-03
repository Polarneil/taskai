from dotenv import load_dotenv
import os
import requests
from requests.auth import HTTPBasicAuth
from crewai.tools import tool

load_dotenv()

jira_api_key = os.getenv('JIRA_API_KEY')
jira_email = os.getenv('JIRA_EMAIL')
jira_url = os.getenv('JIRA_URL')


@tool("JiraIssueDataTool")
def get_issue_data(ticket_key: str) -> dict:
    """Extracts data from a Jira issue given the ticket key"""
    try:
        url = f"{jira_url}/rest/api/3/issue/{ticket_key}"

        auth = HTTPBasicAuth(username=jira_email, password=jira_api_key)

        headers = {
            "Accept": "application/json"
        }

        response = requests.request(
            method="GET",
            url=url,
            headers=headers,
            auth=auth,
        )

        response.raise_for_status()

        response_dict = response.json()

        ticket_info = {
            "id": response_dict.get("id"),
            "key": response_dict.get("key"),
            "summary": response_dict["fields"].get("summary"),
            "description": extract_text_from_description(response_dict["fields"].get("description")),
            "acceptance_criteria": extract_text_from_content(response_dict["fields"].get("customfield_10037")),
            "priority": response_dict["fields"].get("priority", {}).get("name"),
            "assignee": {
                "displayName": response_dict["fields"].get("assignee", {}).get("displayName"),
                "emailAddress": response_dict["fields"].get("assignee", {}).get("emailAddress")
            },
            "reporter": {
                "displayName": response_dict["fields"].get("reporter", {}).get("displayName"),
                "emailAddress": response_dict["fields"].get("reporter", {}).get("emailAddress")
            },
            "issuetype": response_dict["fields"].get("issuetype", {}).get("name"),
            "labels": response_dict["fields"].get("labels"),
        }

        return ticket_info

    except requests.exceptions.HTTPError as e:
        return {"message": f"HTTP error getting issue data for {ticket_key}: {e}"}
    except requests.exceptions.ConnectionError as e:
        return {"message": f"Connection error getting issue data for {ticket_key}: {e}"}
    except requests.exceptions.RequestException as e:
        return {"message": f"Request error getting issue data for {ticket_key}: {e}"}
    except KeyError as e:
        return {"message": f"KeyError getting issue data for {ticket_key}: {e}"}
    except Exception as e:
        return {"message": f"An unexpected error occurred getting issue data for {ticket_key}: {e}"}


def extract_text_from_description(data):
    """
    Extracts all text content from the Jira description field.
    """
    if not isinstance(data, dict) or "content" not in data:
        return ""

    content_list = data["content"]
    extracted_texts = []

    def _extract_recursive(content):
        if isinstance(content, list):
            for item in content:
                _extract_recursive(item)
        elif isinstance(content, dict):
            if "text" in content and content["type"] == "text":
                extracted_texts.append(content["text"])
            elif "content" in content:
                _extract_recursive(content["content"])

    _extract_recursive(content_list)
    return "".join(extracted_texts)


def extract_text_from_content(data):
    """
    Extracts text content from a JSON structure with a 'content' field.

    Args:
        data: A dictionary representing the JSON data.

    Returns:
        A list of strings containing the extracted text.
    """
    if not isinstance(data, dict) or "content" not in data:
        return []

    content_list = data["content"]
    extracted_texts = []

    def _extract_recursive(content):
        if isinstance(content, list):
            for item in content:
                _extract_recursive(item)
        elif isinstance(content, dict):
            if "text" in content and content["type"] == "text":
                extracted_texts.append(content["text"])
            elif "content" in content:
                _extract_recursive(content["content"])

    _extract_recursive(content_list)
    return extracted_texts
