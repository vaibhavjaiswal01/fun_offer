from __future__ import annotations

from typing import Any

from deal_scraper.scrapers import get_scraper
from deal_scraper.telegram_client import TelegramDealClient


def scrape_url(url: str) -> dict[str, Any]:
    scraper = get_scraper(url)
    product = scraper.scrape(url)
    return product.to_dict()


def scrape_urls(urls: list[str]) -> list[dict[str, Any]]:
    results = []
    for url in urls:
        try:
            results.append(scrape_url(url))
        except Exception as exc:  # noqa: BLE001
            results.append({"url": url, "error": str(exc)})
    return results


def scrape_telegram_channel(channel: str, limit: int = 10) -> list[dict[str, Any]]:
    telegram_client = TelegramDealClient()
    messages = telegram_client.fetch_messages(channel=channel, limit=limit)
    items: list[dict[str, Any]] = []
    for message in messages:
        scraped_products = scrape_urls(message.urls)
        items.append(
            {
                "message_id": message.message_id,
                "channel": message.channel,
                "timestamp": message.timestamp,
                "text": message.text,
                "urls": message.urls,
                "products": scraped_products,
            }
        )
    return items
