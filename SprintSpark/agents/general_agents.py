from crewai import Agent
from textwrap import dedent
from SprintSpark.llm.llm import MODELS


class IssueAgents:
    def __init__(self):
        self.models = MODELS()

    def processor_router_agent(self):
        return Agent(
            role="Jira Issue Processor",
            backstory=dedent(f"""You have worked in project management for your entire career."""),
            goal=dedent(f"""Your goal is to analyze a Jira ticket and delegate the issue to the appropriate SME 
            agents."""),
            allow_delegation=False,
            verbose=True,
            llm=self.models.CLAUDE3_7SONNET,
        )

    def collector_reporter_agent(self):
        return Agent(
            role="Data Collector",
            backstory=dedent(f"""You have worked in data collection for your entire career."""),
            goal=dedent(
                f"""
                Your goal is to fetch necessary data from a Jira ticket and various task outputs to feed a report that
                you will generate based on the data.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.models.CLAUDE3_7SONNET,
        )
