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
