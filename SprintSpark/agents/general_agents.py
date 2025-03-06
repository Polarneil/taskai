from crewai import Agent
from textwrap import dedent
from SprintSpark.llm.llm import LLM


class IssueAgents:
    def __init__(self):
        self.models = LLM()

    def processor_router_agent(self):
        return Agent(
            role="Jira Issue Processor",
            backstory=dedent(f"""You have worked in project management for your entire career."""),
            goal=dedent(f"""Your goal is to analyze a Jira ticket and delegate the issue to the appropriate SME 
            agents."""),
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def collector_agent(self):
        return Agent(
            role="Data Collector",
            backstory=dedent(f"""You have worked in data collection for your entire career."""),
            goal=dedent(
                f"""
                Your goal is to fetch necessary data from a Jira ticket and various task outputs to feed a Reporter
                Agent who will generate a report based on the data you fetched.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def reporter_agent(self):
        return Agent(
            role="Reporter",
            backstory=dedent(f"""You are providing a developer with a head start on a Jira issue assigned to them."""),
            goal=dedent(
                f"""
                Your goal is to cohesive summary of the subtask outputs so that the developer can be provided with a
                head start on the Jira issue assigned to them. You will make sure your summary ties back to the initial
                Jira issue fetched from the Collector Agent.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )
