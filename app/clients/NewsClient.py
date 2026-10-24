import httpx
from bs4 import BeautifulSoup
from app.models.Message import MessageClass
import os
from dotenv import load_dotenv
from pathlib import Path
import asyncio
load_dotenv()


class NewsClientClass():
    # azért kell nekünk, mert sokan a botokat letíltják, és így rendes felhsználónak tűnünk
    HEADERS = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
        }

    API_KEY = os.getenv("GNEWS_API_KEY")

    urls: list[str] = []
    """
    async def search_for_news(self, topic: str, language: str, limit: int):
        return ["https://www.hindustantimes.com/cities/lucknow-news/how-the-aliganj-fake-call-centre-in-lucknow-trapped-us-victims-101789831325556.html",
                            "https://www.bgr.com/2257582/is-google-chrome-more-secure-microsoft-edge/"]
    """ 
    async def search_for_news(self, topic: str, language: str, limit: int):


        self.urls: list[str] = []

        base_url = os.getenv("GNEWS_URL")

        if not base_url.endswith("?"):
            base_url += "?"

        url: str = f"{base_url}q={topic.value}&lang={language.value}&max={limit}&apikey={self.API_KEY}"

        async with httpx.AsyncClient() as client:

            response = await client.get(url)

            response.raise_for_status()

            data = response.json()


        for index in data["articles"]:
           self.urls.append(index["url"])
        
        return self.urls
    
    async def get_full_news(self, url_list) -> list[MessageClass]:       
        timeout = httpx.Timeout(
        12.0,
        connect=20.0
        )

        async with httpx.AsyncClient(
            headers=self.HEADERS,
            timeout=timeout,
            follow_redirects=True,
            limits=httpx.Limits(
                max_connections=10,
                max_keepalive_connections=5
            )
        ) as client:
            tasks = [
                self._get_single_news(client, url)
                for url in url_list
            ]

            results = await asyncio.gather(*tasks)

        return [news for news in results if news is not None]

    async def _get_single_news(
        self,
        client: httpx.AsyncClient,
        url: str
    ) -> MessageClass | None:
        try:
            response = await client.get(url)
            response.raise_for_status()

            soup = BeautifulSoup(response.text, "html.parser")

            title_element = soup.find("h1")

            if title_element:
                title = title_element.get_text(strip=True)
            elif soup.title:
                title = soup.title.get_text(strip=True)
            else:
                title = "Unknown title"

            for trash in soup(
                ["script", "style", "nav", "footer", "header", "aside"]
            ):
                trash.decompose()

            paragraphs = soup.find_all("p")
            clean_lines = self.clean_paragraphs(paragraphs)
            full_text = "\n\n".join(clean_lines)

            if not full_text:
                return None

            return MessageClass(title, url, full_text)

        except httpx.HTTPStatusError as e:
            print(f"HTTP hiba ({e.response.status_code}): {url}")
            return None
        except httpx.RequestError as e:
            print(f"Hálózati hiba: {url} — {e}")
            return None
        except Exception as e:
            print(f"Feldolgozási hiba: {url} — {e}")
            return None

    def clean_paragraphs(self, paragraphs):
        for paragraph in paragraphs:
            line = paragraph.get_text(strip=True)
            if(len(line) > 30):
                yield line