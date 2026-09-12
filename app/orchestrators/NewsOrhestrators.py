from app.logging.ProjectLogger import ProjectLoggerClass
from app.formatters.NewsDataFormater import NewsDataFormaterClass
from app.clients.NewsClient import NewsClientClass
from app.Agent.LlmClient import LlmClientClass

class NewsOrhestratorsClass():

    def __init__(self, 
                 projectlogger: ProjectLoggerClass,
                 formaters: NewsDataFormaterClass,
                 newsclient: NewsClientClass,
                 llmclient: LlmClientClass):
        
        self.projectlogger = projectlogger
        self.formaters = formaters
        self.newsclient = newsclient
        self.llmclient = llmclient

    async def execute_pipeline(self, 
                        category: str,
                        language: str,
                        limit: int):
        return f"This is the Category: {category}\nand this is the language: {language}\nand finally, the number of news: {limit}"
    