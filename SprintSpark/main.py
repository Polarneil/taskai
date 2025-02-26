from crewai import Crew
import os
from dotenv import load_dotenv
from textwrap import dedent
from agents.agents import IssueAgents
from tasks.tasks import IssueTasks
from crewai.knowledge.source.string_knowledge_source import StringKnowledgeSource

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")

# Create knowledge source
directions = "You will NOT include triple backticks (```) in any of your inputs or outputs."
direction_source = StringKnowledgeSource(
    content=directions,
)


class SprintSparkCrew:
    def __init__(self, ticket_key: str):
        self.ticket_key = ticket_key

    def run(self):
        # Instantiate agents and tasks
        agents = IssueAgents()
        tasks = IssueTasks()

        # Define agents
        processor_router_agent = agents.processor_router_agent()

        # Define tasks
        fetch_issue_data_task = tasks.fetch_issue_data_task(
            processor_router_agent,
            self.ticket_key,
        )

        decompose_issue_task = tasks.decompose_issue_task(
            processor_router_agent
        )

        # Define crew
        crew = Crew(
            agents=[processor_router_agent],
            tasks=[fetch_issue_data_task, decompose_issue_task],
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
