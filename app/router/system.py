from fastapi import APIRouter, FastAPI, Depends
from app.Agent.LlmClient import LlmClientClass
from app.clients.NewsClient import NewsClientClass
from app.formatters.NewsDataFormater import NewsDataFormaterClass
from app.logging.ProjectLogger import ProjectLoggerClass
from app.orchestrators.NewsOrhestrators import NewsOrhestratorsClass

router = APIRouter(prefix="/news", tags=["get"])

llmclient: LlmClientClass = LlmClientClass()
projectlogger: ProjectLoggerClass = ProjectLoggerClass()
newsclient: NewsClientClass = NewsClientClass()
newsdataformater: NewsDataFormaterClass = NewsDataFormaterClass()

def get_news_service():
    return NewsOrhestratorsClass(
        projectlogger,
        newsdataformater,
        newsclient,
        llmclient
    )


@router.get("/")
async def get_is_summary(category: str, 
                         language: str, 
                         limit: int, 
                         orhestrator: NewsOrhestratorsClass = Depends(get_news_service)):

    
    return await orhestrator.execute_pipeline(category, language, limit)
