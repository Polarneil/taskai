from crewai import Crew
import os
from dotenv import load_dotenv
from textwrap import dedent

from agents.general_agents import IssueAgents
from agents.technical_agents import TechnicalAgents

from tasks.general_tasks import IssueTasks
from tasks.technical_tasks import TechnicalTasks

from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create knowledge source
directions = dedent(
    f"""
    - You will NOT include triple backticks (```) in any of your inputs or outputs.
    """
)
direction_source = StringKnowledgeSource(
    content=directions,
)


class SprintSparkCrew:
    def __init__(self, ticket_key: str):
        self.ticket_key = ticket_key

    def run(self):
        # Instantiate agents and tasks
        general_agents = IssueAgents()
        general_tasks = IssueTasks()

        technical_agents = TechnicalAgents()
        technical_tasks = TechnicalTasks()

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

        analyze_repo_task = technical_tasks.delegate_subtasks_task(
            technical_analyst_agent
        )

        # Define crew
        crew = Crew(
            agents=[processor_router_agent, technical_analyst_agent],
            tasks=[fetch_issue_data_task, decompose_issue_task, analyze_repo_task],
            knowledge_sources=[direction_source],
            verbose=True,
        )

        result = crew.kickoff()
        return result


# Call the crew
if __name__ == "__main__":
    tick_key = input(dedent("""Enter your ticket key: """))

    sprint_spark_crew = SprintSparkCrew(tick_key)
    results = sprint_spark_crew.run()
    print("\n########################")
    print("## Results:")
    print("########################\n")
    print(results)
