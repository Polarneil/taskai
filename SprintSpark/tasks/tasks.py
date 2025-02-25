from crewai import Task
from textwrap import dedent


class IssueTasks:
    def fetch_issue_data_task(self, agent, ticket_key: str):

        return Task(
            description=dedent(
                f"""
                Your task is to fetch data on a given Jira issue. You will do this by calling the `get_issue_data`
                function from the `JiraIssueDataTool`.
                
                This function takes in a single parameter as a string, `ticket_key`. You can find this parameter below.    

                ticket_key={ticket_key}
                """
            ),
            expected_output="The expected output of the task is the data returned from the tool and a brief analysis of the task at hand.",
            agent=agent,
        )
