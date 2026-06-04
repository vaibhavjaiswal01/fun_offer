from __future__ import annotations

import json
from abc import ABC, abstractmethod
from typing import Any
from urllib.parse import urlparse

import requests
from bs4 import BeautifulSoup

from deal_scraper.config import settings
from deal_scraper.models import ProductInfo


class BaseScraper(ABC):
    site_name = "generic"

    def __init__(self) -> None:
        self.session = requests.Session()
        self.session.headers.update(
            {
                "User-Agent": settings.user_agent,
                "Accept-Language": "en-IN,en;q=0.9,en-US;q=0.8",
            }
        )

    def fetch(self, url: str) -> tuple[requests.Response, BeautifulSoup]:
        response = self.session.get(url, timeout=settings.request_timeout, allow_redirects=True)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "lxml")
        return response, soup

    def build_product(
        self,
        *,
        source_url: str,
        response: requests.Response,
        soup: BeautifulSoup,
        overrides: dict[str, Any] | None = None,
    ) -> ProductInfo:
        overrides = overrides or {}
        metadata = self.extract_metadata(soup)
        parsed = urlparse(response.url)
        data = {
            "source_url": source_url,
            "resolved_url": response.url,
            "domain": parsed.netloc,
            "site_name": self.site_name,
            "title": overrides.get("title") or metadata.get("title"),
            "brand": overrides.get("brand") or metadata.get("brand"),
            "price": overrides.get("price") or metadata.get("price"),
            "currency": overrides.get("currency") or metadata.get("currency"),
            "image_url": overrides.get("image_url") or metadata.get("image_url"),
            "description": overrides.get("description") or metadata.get("description"),
            "availability": overrides.get("availability") or metadata.get("availability"),
            "rating": overrides.get("rating") or metadata.get("rating"),
            "raw_metadata": metadata,
        }
        return ProductInfo(**data)

    def extract_metadata(self, soup: BeautifulSoup) -> dict[str, Any]:
        metadata: dict[str, Any] = {}
        metadata.update(self._extract_open_graph(soup))
        metadata.update(self._extract_json_ld(soup))
        return metadata

    def _extract_open_graph(self, soup: BeautifulSoup) -> dict[str, Any]:
        og_map = {
            "og:title": "title",
            "og:description": "description",
            "og:image": "image_url",
            "product:price:amount": "price",
            "product:price:currency": "currency",
            "og:site_name": "site_name",
        }
        data: dict[str, Any] = {}
        for prop, key in og_map.items():
            tag = soup.find("meta", attrs={"property": prop}) or soup.find(
                "meta", attrs={"name": prop}
            )
            if tag and tag.get("content"):
                data[key] = tag["content"].strip()
        return data

    def _extract_json_ld(self, soup: BeautifulSoup) -> dict[str, Any]:
        result: dict[str, Any] = {}
        scripts = soup.find_all("script", attrs={"type": "application/ld+json"})
        for script in scripts:
            raw_text = script.string or script.get_text(strip=True)
            if not raw_text:
                continue
            try:
                payload = json.loads(raw_text)
            except json.JSONDecodeError:
                continue
            candidate = self._find_product_node(payload)
            if not candidate:
                continue
            offers = candidate.get("offers", {}) if isinstance(candidate, dict) else {}
            aggregate_rating = (
                candidate.get("aggregateRating", {}) if isinstance(candidate, dict) else {}
            )
            result.update(
                {
                    "title": candidate.get("name"),
                    "brand": self._extract_brand(candidate),
                    "description": candidate.get("description"),
                    "image_url": self._extract_image(candidate),
                    "price": self._extract_offer_value(offers, "price"),
                    "currency": self._extract_offer_value(offers, "priceCurrency"),
                    "availability": self._extract_offer_value(offers, "availability"),
                    "rating": self._extract_offer_value(aggregate_rating, "ratingValue"),
                }
            )
            break
        return {key: value for key, value in result.items() if value}

    def _find_product_node(self, payload: Any) -> dict[str, Any] | None:
        if isinstance(payload, dict):
            node_type = payload.get("@type")
            if node_type == "Product" or (isinstance(node_type, list) and "Product" in node_type):
                return payload
            for key in ("@graph", "mainEntity", "itemListElement"):
                nested = payload.get(key)
                found = self._find_product_node(nested)
                if found:
                    return found
        if isinstance(payload, list):
            for item in payload:
                found = self._find_product_node(item)
                if found:
                    return found
        return None

    def _extract_brand(self, candidate: dict[str, Any]) -> str | None:
        brand = candidate.get("brand")
        if isinstance(brand, dict):
            return brand.get("name")
        if isinstance(brand, str):
            return brand
        return None

    def _extract_image(self, candidate: dict[str, Any]) -> str | None:
        image = candidate.get("image")
        if isinstance(image, list) and image:
            return str(image[0])
        if isinstance(image, str):
            return image
        return None

    def _extract_offer_value(self, offers: Any, key: str) -> str | None:
        if isinstance(offers, list) and offers:
            first = offers[0]
            if isinstance(first, dict):
                value = first.get(key)
                return str(value) if value is not None else None
        if isinstance(offers, dict):
            value = offers.get(key)
            return str(value) if value is not None else None
        return None

    def find_text(self, soup: BeautifulSoup, selectors: list[str]) -> str | None:
        for selector in selectors:
            node = soup.select_one(selector)
            if node:
                text = node.get_text(" ", strip=True)
                if text:
                    return text
        return None

    def find_attr(self, soup: BeautifulSoup, selectors: list[str], attribute: str) -> str | None:
        for selector in selectors:
            node = soup.select_one(selector)
            if node and node.get(attribute):
                value = str(node.get(attribute)).strip()
                if value:
                    return value
        return None

    @abstractmethod
    def scrape(self, url: str) -> ProductInfo:
        raise NotImplementedError
