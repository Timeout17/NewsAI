from app.models.Message import MessageClass
from app.Agent.CreateAgent import CreateAgentClass
from app.Agent.CreateMessage import CreateMessageClass
import os
from dotenv import load_dotenv
from groq import RateLimitError
from typing import Optional


load_dotenv()


class LLMOrhestratorsClass():

    def __init__(self):
        self.client = CreateAgentClass().create_client()
        self.messagefactory = CreateMessageClass()

    async def Chatservice(self, messages: list[MessageClass], language: str) -> Optional[list[str]]:
        answer: list[str] = []
        for message in messages:
            prompt = self.messagefactory.create_message(message.content, language, message.url, message.title)

            try:
                response = self.client.chat.completions.create(
                    model=os.environ.get("MODEL"),
                    messages=prompt,
                    temperature=0.5,
                    max_completion_tokens=4096
                )

                answer.append(response.choices[0].message.content)

            except RateLimitError as e:
                print("API limit overloaded")
                print(e)

                return None

        return answer            
