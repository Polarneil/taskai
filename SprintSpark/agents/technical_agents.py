from crewai import Agent
from textwrap import dedent
from langchain_openai import ChatOpenAI


class TechnicalAgents:
    def __init__(self):
        self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo", temperature=0.7)
        self.OpenAIGPT4o = ChatOpenAI(model_name="gpt-4o", temperature=0.7)
        self.OpenAIGPT4omini = ChatOpenAI(model_name="gpt-4o-mini", temperature=0.7)
        self.Ollama = ChatOpenAI(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434"
        )

    def technical_analyst_agent(self):
        return Agent(
            role="Technical Analyst",
            backstory=dedent(f"""You have spent your career analyzing technical tasks and assigning them.."""),
            goal=dedent(
                f"""
                Your goal is to analyze the subtasks at hand from the Jira Issue Processor and assign them to the proper
                tehnical SME.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.OpenAIGPT4o,
        )
