from crewai import Crew
from dotenv import load_dotenv
from textwrap import dedent
import os

from langtrace_python_sdk import langtrace

from agents.general_agents import IssueAgents
from agents.technical_agents import TechnicalAgents

from tasks.general_tasks import IssueTasks
from tasks.technical_tasks import TechnicalTasks

from tools.AttachNotifyTool import UserDelivery

load_dotenv()

# langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))


class SprintSparkCrew:
    def __init__(
            self,
            ticket_key: str,
            email: str,

            github_owner: str,
            github_repo: str,
            base_branch: str,
            github_token: str,

            local_report_path: str,
    ):
        self.ticket_key = ticket_key
        self.email = email

        self.github_owner = github_owner
        self.github_repo = github_repo
        self.base_branch = base_branch
        self.github_token = github_token

        self.local_report_path = local_report_path

    def run(self):
        # Instantiate agents and tasks
        general_agents = IssueAgents()
        general_tasks = IssueTasks()
        technical_agents = TechnicalAgents()

        sme_agents = {
            "Software Engineering SME": technical_agents.software_engineering_sme(),
            "Data SME": technical_agents.data_sme(),
            "Cloud Infrastructure SME": technical_agents.cloud_infrastructure_sme(),
            "Mobile SME": technical_agents.mobile_sme(),
            "Security SME": technical_agents.security_sme(),
            "UI/XD SME": technical_agents.ui_xd_sme(),
        }

        technical_tasks = TechnicalTasks(sme_agents)

        # Define agents
        processor_router_agent = general_agents.processor_router_agent()
        technical_analyst_agent = technical_agents.technical_analyst_agent()

        # Define tasks
        fetch_issue_data_task = general_tasks.fetch_issue_data_task(
            processor_router_agent,
            self.ticket_key,
        )

        decompose_issue_task = general_tasks.decompose_issue_task(
            processor_router_agent
        )

        delegate_task = technical_tasks.delegate_subtasks_task(technical_analyst_agent)

        # Run crew to delegate tasks
        delegation_crew = Crew(
            agents=[processor_router_agent, technical_analyst_agent],
            tasks=[fetch_issue_data_task, decompose_issue_task, delegate_task],
            verbose=True,
        )

        delegation_result = delegation_crew.kickoff()

        # Get SME tasks based on delegation output
        assigned_sme_tasks = technical_tasks.assign_sme_tasks(delegation_result)

        if not assigned_sme_tasks:
            print("No subtasks were assigned to SMEs.")
            return delegation_result

        # Create SME crew
        sme_crew = Crew(
            agents=list(sme_agents.values()),  # Add all SME agents
            tasks=assigned_sme_tasks,  # Assign dynamically created SME tasks
            verbose=True,
        )

        sme_crew.kickoff()

        # Deliverable Crew

        collector_agent = general_agents.collector_reporter_agent()

        fetch_issue_data_task_1 = general_tasks.fetch_issue_data_task_1(
            collector_agent,
            self.ticket_key
        )

        fetch_subtask_output_task = general_tasks.fetch_subtask_output_task(collector_agent)

        generate_report_task = general_tasks.generate_report_task(collector_agent)

        deliverable_crew = Crew(
            agents=[collector_agent],
            tasks=[fetch_issue_data_task_1, fetch_subtask_output_task, generate_report_task],
            verbose=True,
        )

        deliverable_results = deliverable_crew.kickoff()

        # Attach and notify user
        try:
            with open(self.local_report_path, 'r') as file:
                file_content = file.read()
        except FileNotFoundError:
            print(f"Error: File not found at {self.local_report_path}")
            file_content = None

        deliverer = UserDelivery(
            github_owner=self.github_owner,
            github_repo=self.github_repo,
            branch_name=f"feature/{self.ticket_key}",
            base_branch=self.base_branch,
            repo_file_path=f"TaskAI_Summary_Reports/{self.ticket_key}_report.md",
            file_content=file_content,
            commit_message=f"TaskAI Summary Report: {self.ticket_key}",
            github_token=self.github_token,

            ticket_key=self.ticket_key,
            receiver_email=self.email,
            subject=f"Summary Report for {self.ticket_key}",
            message=f"Please find the summary report for {self.ticket_key} attached.",
            file_path=self.local_report_path,
        )

        deliverer.attach_and_notify()

        return deliverable_results


# Call the crew
if __name__ == "__main__":

    github_owner = os.getenv("GITHUB_OWNER")
    github_repo = os.getenv("GITHUB_REPO")
    base_branch = os.getenv("GITHUB_BASE_BRANCH")
    github_token = os.getenv("GITHUB_TOKEN")

    local_report_path = "./summary_reports/report.md"

    tick_key = input(dedent("""Enter your ticket key: """))
    user_email = input(dedent("""Enter your email: """))

    sprint_spark_crew = SprintSparkCrew(
        ticket_key=tick_key,
        email=user_email,

        github_owner=github_owner,
        github_repo=github_repo,
        base_branch=base_branch,
        github_token=github_token,

        local_report_path=local_report_path
    )

    results = sprint_spark_crew.run()
    print("\n########################")
    print("## Results:")
    print("########################\n")
    print(results)
