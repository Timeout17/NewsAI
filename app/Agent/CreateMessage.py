from app.models.Enum import Roles

class CreateMessageClass():

    @staticmethod
    def create_message(message: str, language: str):
        return [
            {
                "role": Roles.SYSTEM.value,
                "content":f"""
                    kapni fogsz, angol más nyelvű szövegeket, ezeket fordítse le: {language}
                    Ezeket a hírekeket rövidísd is le, csak a lényeget írd ki belőlük, kb 5-6 mondatban legyenek.
                    """
            },

            {
                "role": Roles.USER.value,
                "content": message
            }
        ]