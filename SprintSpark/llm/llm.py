from crewai import LLM
from dotenv import load_dotenv
import os

load_dotenv()


class MODELS:
    def __init__(self):
        self.OpenAIGPT35 = LLM(
            model="gpt-3.5-turbo",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.OpenAIGPT4o = LLM(
            model="gpt-4o",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.OpenAIGPTo3mini = LLM(
            model="o3-mini",
            temperature=0.7,
            api_key=os.getenv("OPENAI_API_KEY"),
        )
        self.Gemini2Flash = LLM(
            model='gemini/gemini-2.0-flash',
            api_key=os.getenv("GEMINI_API_KEY"),
        )
        self.LLAMA_3_1_8B = LLM(
            model="ollama/llama3.1:8b",
            base_url="http://localhost:11434",
        )
        self.CLAUDE3_7SONNET = LLM(
            model="bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0",
        )
