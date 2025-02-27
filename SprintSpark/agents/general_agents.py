from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


class IssueAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.OpenAIGPT4omini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def processor_router_agent(self):
        return Agent(
            role="Jira Issue Processor",
            backstory=dedent(f"""You have worked in project management for your entire career."""),
            goal=dedent(f"""Your goal is to analyze a Jira ticket and delegate the issue to the appropriate SME 
            agents."""),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )
