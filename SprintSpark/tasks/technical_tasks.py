from crewai import Task
from textwrap import dedent
import ast
from SprintSpark.tools.CrawlRepoTool import crawl_repo_to_dict


class TechnicalTasks:
    def __init__(self, sme_agents):
        self.sme_agents = sme_agents  # Dictionary mapping SME names to agents

    def delegate_subtasks_task(self, agent):
        return Task(
            description=dedent(
                f"""
                Your task is to analyze the Jira issue and its subtasks, then assign each subtask to the most
                relevant technical SME agent from the available options. 
                
                If certain subtasks are similar to one another or involve modify what would be the same code file, 
                you should bundle them up as one task.
                
                In essence, we should not have seperate tasks iterating on the same file.

                Available Technical SME Agents:
                {', '.join(self.sme_agents.keys())}

                You will NOT route a subtask to an agent that does not exist in the list above.
                
                Ensure the subtasks (keys) are extremely detailed as the SME agents will not be able to access the 
                original Jira issue.
                """
            ),
            expected_output=dedent(
                f"""
                Return a structured JSON assignment of subtasks and acceptance criteria to the appropriate SME agents.
                
                You will NOT use triple backticks in your response.
                
                Example:

                {{
                    "subtask & acceptance criteria": "Security SME",
                    "subtask & acceptance criteria": "Data SME"
                }}
                """
            ),
            agent=agent,
            output_processing=self.assign_sme_tasks  # This will distribute tasks dynamically
        )

    def assign_sme_tasks(self, crew_output):
        """
        Parses the delegation output and creates tasks for assigned SME agents.
        """
        try:
            # Extract the result as a dictionary
            crew_dict = ast.literal_eval(crew_output.raw)

            if not isinstance(crew_dict, dict):
                raise ValueError("Expected delegation output to be a dictionary.")

            sme_tasks = []
            i = 0
            for subtask, sme_name in crew_dict.items():
                if sme_name not in self.sme_agents:
                    print(f"Warning: SME '{sme_name}' not recognized, skipping task '{subtask}'.")
                    continue
                i += 1
                sme_agent = self.sme_agents[sme_name]
                sme_task = Task(
                    description=dedent(
                        f"""
                        Work on subtask: {subtask}
                        
                        You will utilize the git repo and ensure your solutions fit in with the current project
                        structure. You will call the `crawl_repo_to_dict` function from the `CrawlRepoTool` to analyze
                        the repository. You do not need to pass any arguments into this function.
                        """
                    ),
                    tools=[crawl_repo_to_dict],
                    expected_output="Provide the completed work for this subtask. Provide any code files/snippets if applicable. Format your responses in markdown.",
                    output_file=f"/outputs/subtask_{i}.txt",
                    agent=sme_agent,
                )
                sme_tasks.append(sme_task)

            return sme_tasks

        except Exception as e:
            print(f"Error processing delegation output: {e}")
            return []
