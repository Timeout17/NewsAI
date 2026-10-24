
from unittest.mock import AsyncMock, Mock

import pytest

from app.orchestrators.NewsOrhestrators import NewsOrhestratorsClass


@pytest.mark.asyncio
async def test_execute_pipeline_returns_joined_summaries():
    # Arrange: előkészítjük a függőségeket
    logger = Mock()
    formatter = Mock()

    news_client = Mock()
    news_client.search_for_news = AsyncMock(return_value=["url1", "url2"])
    news_client.get_full_news = AsyncMock(return_value=["article1", "article2"])

    llm_orchestrator = Mock()
    llm_orchestrator.Chatservice = AsyncMock(
        return_value=["summary1", "summary2"]
    )

    orchestrator = NewsOrhestratorsClass(
        logger,
        formatter,
        news_client,
        llm_orchestrator,
    )

    # Act: lefuttatjuk a pipeline-t
    result = await orchestrator.execute_pipeline(
        category="Nation",
        language="Hungarian",
        limit=2,
    )

    # Assert: ellenőrizzük az eredményt és a hívásokat
    assert result == "summary1\n\nsummary2"

    news_client.search_for_news.assert_awaited_once_with(
        topic="Nation",
        language="Hungarian",
        limit=2,
    )
    news_client.get_full_news.assert_awaited_once_with(
        ["url1", "url2"]
    )
    llm_orchestrator.Chatservice.assert_awaited_once_with(
        ["article1", "article2"],
        "Hungarian",
    )


@pytest.mark.asyncio
async def test_pipeline_stops_when_news_search_fails():
    logger = Mock()
    formatter = Mock()

    news_client = Mock()
    news_client.search_for_news = AsyncMock(
        side_effect=RuntimeError("GNews unavailable")
    )

    llm_orchestrator = Mock()
    llm_orchestrator.Chatservice = AsyncMock()

    orchestrator = NewsOrhestratorsClass(
        logger, formatter, news_client, llm_orchestrator
    )

    with pytest.raises(RuntimeError, match="GNews unavailable"):
        await orchestrator.execute_pipeline(
            category="Nation",
            language="Hungarian",
            limit=2,
        )

    llm_orchestrator.Chatservice.assert_not_awaited()



@pytest.mark.asyncio
async def test_pipeline_returns_empty_string_when_no_news_found():
    logger = Mock()
    formatter = Mock()

    news_client = Mock()
    news_client.search_for_news = AsyncMock(return_value=[])
    news_client.get_full_news = AsyncMock(return_value=[])

    llm_orchestrator = Mock()
    llm_orchestrator.Chatservice = AsyncMock()
    llm_orchestrator.Chatservice = AsyncMock(return_value=[])

    orchestrator = NewsOrhestratorsClass(
        logger, formatter, news_client, llm_orchestrator
    )

    result = await orchestrator.execute_pipeline(
        category="Nation",
        language="Hungarian",
        limit=2,
    )

    assert result == ""
    llm_orchestrator.Chatservice.assert_awaited_once_with([], "Hungarian")



@pytest.mark.asyncio
async def test_pipeline_raises_when_llm_returns_none():
    logger = Mock()
    formatter = Mock()

    news_client = Mock()
    news_client.search_for_news = AsyncMock(return_value=["url1"])
    news_client.get_full_news = AsyncMock(return_value=["article1"])

    llm_orchestrator = Mock()
    llm_orchestrator.Chatservice = AsyncMock()
    llm_orchestrator.Chatservice = AsyncMock(return_value=None)

    orchestrator = NewsOrhestratorsClass(
        logger, formatter, news_client, llm_orchestrator
    )

    with pytest.raises(TypeError):
        await orchestrator.execute_pipeline(
            category="Nation",
            language="Hungarian",
            limit=1,
        )
