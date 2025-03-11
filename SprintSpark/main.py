from crewai import Crew
import os
from dotenv import load_dotenv
from textwrap import dedent

from langtrace_python_sdk import langtrace

from agents.general_agents import IssueAgents
from agents.technical_agents import TechnicalAgents

from tasks.general_tasks import IssueTasks
from tasks.technical_tasks import TechnicalTasks

from tools.AttachNotifyTool import attach_and_notify

load_dotenv()

# langtrace.init(api_key=os.getenv("LANGTRACE_API_KEY"))

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


class SprintSparkCrew:
    def __init__(self, ticket_key: str, email: str):
        self.ticket_key = ticket_key
        self.email = email

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

        sme_results = sme_crew.kickoff()

        # Deliverable Crew

        collector_agent = general_agents.collector_agent()
        reporter_agent = general_agents.reporter_agent()

        fetch_issue_data_task_1 = general_tasks.fetch_issue_data_task_1(
            collector_agent,
            self.ticket_key
        )

        fetch_subtask_output_task = general_tasks.fetch_subtask_output_task(collector_agent)

        generate_report_task = general_tasks.generate_report_task(reporter_agent)

        deliverable_crew = Crew(
            agents=[collector_agent, reporter_agent],
            tasks=[fetch_issue_data_task_1, fetch_subtask_output_task, generate_report_task],
            verbose=True,
        )

        deliverable_results = deliverable_crew.kickoff()

        # Attach and notify
        attach_and_notify(
            ticket_key=self.ticket_key,
            receiver_email=self.email,
            subject=f"Summary Report for {self.ticket_key}",
            message="Please find the summary report attached.",
        )

        return deliverable_results


# Call the crew
if __name__ == "__main__":
    tick_key = input(dedent("""Enter your ticket key: """))
    email = input(dedent("""Enter your email: """))

    sprint_spark_crew = SprintSparkCrew(tick_key, email)
    results = sprint_spark_crew.run()
    print("\n########################")
    print("## Results:")
    print("########################\n")
    print(results)
