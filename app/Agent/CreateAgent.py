from groq import Groq
import os
from dotenv import load_dotenv

load_dotenv()

class CreateAgentClass():
    @staticmethod
    def create_client():
        return Groq(
                api_key=os.environ.get("GROQ_API_KEY"),
                )

