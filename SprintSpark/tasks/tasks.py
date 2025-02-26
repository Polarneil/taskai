from crewai import Task
from textwrap import dedent
from SprintSpark.tools.JiraIssueDataTool import get_issue_data


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
            tools=[get_issue_data],
            expected_output="The expected output of the task is the raw data returned from the tool.",
            agent=agent,
        )

    def decompose_issue_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to decompose the Jira issue into various subtasks. If the issue is small, do not
                feel the need to decompose any further.
                
                Ensure your subtasks follow development best practices.
                
                You will utilize the output from the `fetch_issue_data_task`.
                """
            ),
            expected_output="The expected output of this tast is a decomposition of the Jira issue.",
            agent=agent,
        )
