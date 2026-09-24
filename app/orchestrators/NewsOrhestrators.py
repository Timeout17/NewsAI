from app.logging.ProjectLogger import ProjectLoggerClass
from app.formatters.NewsDataFormater import NewsDataFormaterClass
from app.clients.NewsClient import NewsClientClass
from app.orchestrators.LLMOrhestrators import LLMOrhestratorsClass

class NewsOrhestratorsClass():

    def __init__(self, 
                 projectlogger: ProjectLoggerClass,
                 formaters: NewsDataFormaterClass,
                 newsclient: NewsClientClass,
                 llmorhestrator: LLMOrhestratorsClass):
        
        self.projectlogger = projectlogger
        self.formaters = formaters
        self.newsclient = newsclient
        self.llmorhestrator = llmorhestrator

    async def execute_pipeline(self, 
                        category: str,
                        language: str,
                        limit: int):
        
        url_list = await self.newsclient.search_for_news(topic=category, language=language, limit=limit)
        news = await self.newsclient.get_full_news(url_list)

        Agentorhestrator = await self.llmorhestrator.Chatservice(news)