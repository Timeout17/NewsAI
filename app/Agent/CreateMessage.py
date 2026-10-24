from app.models.Enum import Roles
from pathlib import Path

class CreateMessageClass():

    PROMPT_DIR = Path(__file__).resolve().parents[2] / "prompts" / "news_summary"

    @staticmethod
    def create_message(message: str, language: str, url: str, title: str):
          system_prompt = (
               CreateMessageClass.PROMPT_DIR / "v2.txt"
          ).read_text(encoding="utf-8")

          user_template = (
               CreateMessageClass.PROMPT_DIR / "user_template.txt"
          ).read_text(encoding="utf-8")

          system_prompt = system_prompt.replace("{language}", language)

          user_prompt = user_template.format(
               title=title,
               url=url,
               message=message
          )

          return [
               {
                    "role": Roles.SYSTEM.value,
                    "content": system_prompt
               },
               {
                    "role": Roles.USER.value,
                    "content": user_prompt
               }
          ]