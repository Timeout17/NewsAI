import requests


def fetch_news(url: str, params: dict):
    response = requests.get(
        url,
        params=params,
        timeout=10
    )

    response.raise_for_status()

    return response.json()