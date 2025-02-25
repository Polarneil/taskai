from crewai import Crew
import os
from dotenv import load_dotenv
from textwrap import dedent
from agents.agents import IssueAgents
from tasks.tasks import IssueTasks

load_dotenv()

os.environ["OPENAI_API_KEY"] = os.getenv("OPENAI_API_KEY")


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

        # Define crew
        crew = Crew(
            agents=[processor_router_agent],
            tasks=[fetch_issue_data_task],
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
