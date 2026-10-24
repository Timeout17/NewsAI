from app.logging.ProjectLogger import ProjectLoggerClass
from app.formatters.NewsDataFormater import NewsDataFormaterClass
from app.clients.NewsClient import NewsClientClass
from app.orchestrators.LLMOrhestrators import LLMOrhestratorsClass
import time
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

        start = time.perf_counter()
        try:

            url_list = await self.newsclient.search_for_news(topic=category, language=language, limit=limit)
        finally:
            print(f"""
            [MÉRÉS] EREDMÉNYE: GNEWS URL-lekérés: ... 
            {time.perf_counter() - start:.2f} másodperc
            """)

        start = time.perf_counter()
        try:

            news = await self.newsclient.get_full_news(url_list)
        finally:
            print(f"""
            [MÉRÉS] EREDMÉNYE: Cikk letöltése, és feldolgozás: ... 
            {time.perf_counter() - start:.2f} másodperc
            """)

        start = time.perf_counter()
        try:

            result = await self.llmorhestrator.Chatservice(news, language)
        finally:
            print(f"""
            [MÉRÉS] EREDMÉNYE: GROQ LLM adatfeldolgozás: ... 
            {time.perf_counter() - start:.2f} másodperc
            """)
                    
        final_result = "\n\n".join(result)

        return final_result

