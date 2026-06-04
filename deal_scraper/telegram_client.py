from __future__ import annotations

import re
from dataclasses import dataclass

from telethon.sync import TelegramClient

from deal_scraper.config import settings

URL_PATTERN = re.compile(r"(https?://\S+)")


@dataclass
class TelegramMessage:
    message_id: int
    channel: str
    text: str
    timestamp: str
    urls: list[str]


class TelegramDealClient:
    def __init__(self) -> None:
        if not settings.telegram_api_id or not settings.telegram_api_hash:
            raise ValueError("Telegram credentials are missing. Set TELEGRAM_API_ID and TELEGRAM_API_HASH.")
        self.client = TelegramClient(
            settings.telegram_session_name,
            int(settings.telegram_api_id),
            settings.telegram_api_hash,
        )

    def fetch_messages(self, channel: str, limit: int = 10) -> list[TelegramMessage]:
        messages: list[TelegramMessage] = []
        with self.client:
            entity = self.client.get_entity(channel)
            for msg in self.client.iter_messages(entity, limit=limit):
                text = msg.text or ""
                urls = URL_PATTERN.findall(text)
                messages.append(
                    TelegramMessage(
                        message_id=msg.id,
                        channel=channel,
                        text=text,
                        timestamp=msg.date.isoformat(),
                        urls=urls,
                    )
                )
        return messages
