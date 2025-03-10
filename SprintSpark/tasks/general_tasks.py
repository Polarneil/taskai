from crewai import Task
from textwrap import dedent
from SprintSpark.tools.JiraIssueDataTool import get_issue_data
from SprintSpark.tools.FetchSubtaskOutputTool import get_text_files


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

    def fetch_issue_data_task_1(self, agent, ticket_key: str):
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

    def fetch_subtask_output_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to fetch the output of various subtasks. You will do this by calling the `get_text_files`
                function from the `FetchSubtaskOutputTool`.
                """
            ),
            tools=[get_text_files],
            expected_output="The expected output of the task is a message indicating success or failure",
            agent=agent,
        )

    def generate_report_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to generate a report based on the data fetched by the Collector Agent. The report should
                be a cohesive summary of the subtask subtask_outputs so that the developer can be provided with a head start on
                the Jira issue assigned to them.
                
                You will leverage the Jira issue data returned from the `fetch_issue_data_task_1` and the subtask outputs
                returned from the `FetchSubtaskOutputTool` in the `fetch_subtask_output_task`.
                """
            ),
            expected_output="The expected output of the task is a cohesive summary of the subtask subtask_outputs formatted in markdown.",
            output_file=f"/summary_reports/report.md",
            agent=agent,
        )
