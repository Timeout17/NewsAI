
from fastapi.testclient import TestClient

from app.main import app
from app.router.system import get_news_service


class FakeNewsService:
    async def execute_pipeline(self, category, language, limit):
        return "Első tesztösszefoglaló\n\nMásodik tesztösszefoglaló"


def override_news_service():
    return FakeNewsService()


app.dependency_overrides[get_news_service] = override_news_service

client = TestClient(app)


def test_latest_news_returns_summary():
    response = client.get(
        "/news/latest",
        params={
            "category": "Nation",
            "language": "Hungarian",
            "limit": 2,
        },
    )

    assert response.status_code == 200
    assert response.json() == (
        "Első tesztösszefoglaló\n\nMásodik tesztösszefoglaló"
    )


def test_latest_news_rejects_zero_limit():
    response = client.get(
        "/news/latest",
        params={
            "category": "Nation",
            "language": "Hungarian",
            "limit": 0,
        },
    )

    assert response.status_code == 422
