from fastapi import APIRouter, Depends, Query
from app.Agent.LlmClient import LlmClientClass
from app.clients.NewsClient import NewsClientClass
from app.formatters.NewsDataFormater import NewsDataFormaterClass
from app.logging.ProjectLogger import ProjectLoggerClass
from app.orchestrators.NewsOrhestrators import NewsOrhestratorsClass
from app.models.Enum import Category, Language
from app.middleware.rate_limiter import rate_limit

router = APIRouter(prefix="/news", tags=["news"])

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


@router.get("/latest")
async def get_is_summary(category: Category, 
                         language: Language, 
                         limit: int = Query(ge=1, le=10), 
                         orhestrator: NewsOrhestratorsClass = Depends(get_news_service),
                         _: None = Depends(rate_limit)):

    # DEBUG SOROK: Ez kiírja a terminálba, hogy mi micsoda valójában!
    print(f"DEBUG - orhestrator típus: {type(orhestrator)}")
    print(f"DEBUG - category érték: {category.value if hasattr(category, 'value') else category}")
    
    # Próbáljuk meg tiszta stringként átadni az Enum értékeket (.value)
    cat_str = category.value if hasattr(category, "value") else category
    lang_str = language.value if hasattr(language, "value") else language

    
    return await orhestrator.execute_pipeline(category, language, limit)
