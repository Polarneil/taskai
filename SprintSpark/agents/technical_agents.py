from crewai import Agent
from textwrap import dedent
from SprintSpark.llm.llm import LLM


class TechnicalAgents:
    def __init__(self):
        self.models = LLM()

    def technical_analyst_agent(self):
        return Agent(
            role="Technical Analyst",
            backstory=dedent(f"""You have spent your career analyzing technical tasks and assigning them.."""),
            goal=dedent(
                f"""
                Your goal is to analyze the subtasks at hand from the Jira Issue Processor and assign them to the proper
                technical SME.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def software_engineering_sme(self):
        return Agent(
            role="Software Engineering SME",
            backstory="You are an expert in software development, coding best practices, and software architecture.",
            goal=dedent(
                f"""
                Your goal is to provide expertise in software engineering and assist in solving related technical
                issues. You will do this by writing code, providing code reviews, and offering technical guidance.
                """
            ),
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def data_sme(self):
        return Agent(
            role="Data SME",
            backstory="You specialize in data engineering, data science, and database management.",
            goal="Your goal is to provide data-related insights and handle data pipeline and analysis tasks.",
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def cloud_infrastructure_sme(self):
        return Agent(
            role="Cloud Infrastructure SME",
            backstory="You have extensive knowledge in cloud platforms, networking, and infrastructure automation.",
            goal="Your goal is to advise on cloud architecture, security, and deployment strategies.",
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def mobile_sme(self):
        return Agent(
            role="Mobile SME",
            backstory=dedent(
                f"""
                You are an expert in mobile app development, covering iOS, Android, and cross-platform frameworks.
                """
            ),
            goal="Your goal is to assist in mobile development best practices and troubleshoot app-related issues.",
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def security_sme(self):
        return Agent(
            role="Security SME",
            backstory="You specialize in cybersecurity, penetration testing, and secure coding practices.",
            goal="Your goal is to ensure security best practices are followed and to mitigate risks.",
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )

    def ui_xd_sme(self):
        return Agent(
            role="UI/UX SME",
            backstory="You are a specialist in user interface design and user experience research.",
            goal="Your goal is to ensure intuitive, accessible, and visually appealing design solutions.",
            allow_delegation=False,
            verbose=True,
            llm=self.models.OpenAIGPT4o,
        )
