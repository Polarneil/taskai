from crewai import Task
from textwrap import dedent


class TechnicalTasks:
    def delegate_subtasks_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to route the sub tasks created from the Jira issue to the appropriate technical SME agent. 
                You can find a list of technical SME agents below.
                
                Technical SME Agents:
                    - Software Engineering SME
                    - Data SME
                    - Cloud Infrastructure SME
                    - Mobile SME
                    - Security SME
                    - UI/XD SME
                    
                Please note that you can route various subtasks to different agents.
                
                You will NOT route a subtask to an agent that does not exist in the list above.
                """
            ),
            expected_output=dedent(
                f"""
                The expected output of this task is a list containing the subtasks and the technical SME agents that
                they have been assigned to. You will also provide brief reasoning as to why you assigned an agent a
                task.
                """
            ),
            agent=agent,
        )
