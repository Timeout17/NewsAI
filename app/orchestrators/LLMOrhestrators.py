from app.models.Message import MessageClass
from app.Agent.CreateAgent import CreateAgentClass
from app.Agent.CreateMessage import CreateMessageClass
import os
from dotenv import load_dotenv
from groq import RateLimitError
from typing import Optional
import asyncio
import time

load_dotenv()

class LLMOrhestratorsClass():

    def __init__(self):
        self.client = CreateAgentClass.create_client()
        self.messagefactory = CreateMessageClass()
        self.semaphore = asyncio.Semaphore(3)

    async def process_one(
        self,
        message: MessageClass,
        language: str
    ) -> str:

        start = time.perf_counter()
        prompt = self.messagefactory.create_message(
            message.content,
            language,
            message.url,
            message.title
        )

        prompt_time = time.perf_counter() - start

        semaphore_time = time.perf_counter()
        async with self.semaphore:

            semaphore_wait = time.perf_counter() - semaphore_time
            api_start = time.perf_counter()
            response = await self.client.chat.completions.create(
                model=os.environ.get("MODEL"),
                messages=prompt,
                temperature=0.5,
                max_completion_tokens=600
            )

            api_time = time.perf_counter() - api_start

            print(
                f"[Groq MÉRÉS] "
                f"prompt={prompt_time:.3f}s | "
                f"semaphore_wait={semaphore_wait:.3f}s | "
                f"api={api_time:.3f}s"
            )

        return response.choices[0].message.content or ""

    async def Chatservice(
        self,
        messages: list[MessageClass],
        language: str
    ) -> Optional[list[str]]:

        try:
            return await asyncio.gather(
                *[
                    self.process_one(message, language)
                    for message in messages
                ],
                return_exceptions=True
            )

        except RateLimitError as e:
            print("API limit overloaded")
            print(e)
            return None
