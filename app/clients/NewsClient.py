import httpx
from bs4 import BeautifulSoup
import os
from dotenv import load_dotenv
load_dotenv()

class NewsClientClass():
    # azért kell nekünk, mert sokan a botokat letíltják, és így rendes felhsználónak tűnünk
    HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    API_KEY = os.getenv("GNEWS_API_KEY")

    urls: list[str] = []

    async def search_for_news(self, topic: str, language: str, limit: int):
        return ["https://www.hindustantimes.com/cities/lucknow-news/how-the-aliganj-fake-call-centre-in-lucknow-trapped-us-victims-101789831325556.html",
                            "https://www.bgr.com/2257582/is-google-chrome-more-secure-microsoft-edge/"]
        

    """

    async def search_for_news(self, topic: str, language: str, limit: int):

        base_url = os.getenv("GNEWS_URL")

        if not base_url.endswith("?"):
            base_url += "?"

        url: str = f"{base_url}q={topic}&lang={language}&max={limit}&apikey={self.API_KEY}"

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            response.raise_for_status()

            data = response.json()


        for index in data["articles"]:
           self.urls.append(index["url"])
        
        return self.urls
    """
    async def get_full_news(self, url_list):

        news: list[str] = []

        for url in url_list:
            try:

                async with httpx.AsyncClient() as client:
                    response = await client.get(url)

                    response.raise_for_status()

                    soup = BeautifulSoup(response.text, "html.parser")


                    for trash in soup(["script", "style", "nav", "footer", "header", "aside"]):
                        trash.decompose()

                    paragraphs = soup.find_all("p")

                    articel_lines = [p.get_text().strip() for p in paragraphs]

                    clean_lines = [line for line in articel_lines if len(line) > 30]

                    full_text = "\n\n".join(clean_lines)

                    if not full_text:
                        return "Nem sikerült szöveges tartalmat kinyerni az oldalból."
                    news.append(full_text)
            except Exception as e:
                return f"Hiba a scraping során: {e}"

        return news

