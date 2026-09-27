from app.models.Enum import Roles

class CreateMessageClass():

    @staticmethod
    def create_message(message: str, language: str, url: str, title: str):
            return [
            {
                "role": Roles.SYSTEM.value,
                "content": f"""
                You will receive a news article.

                Translate the article into {language}.
                Summarize it in approximately 5-6 sentences.
                Include only the most important information.

                Format the response as:

                # TITLE

                URL

                CONTENT

                Highlight important events in bold.
                """
            },
            {
                "role": Roles.USER.value,
                "content": f"""
                Title: {title}
                URL: {url}

                Article:
                {message}
                """
            }
    ]