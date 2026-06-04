from __future__ import annotations

from urllib.parse import urlparse

from deal_scraper.scrapers.ajio import AjioScraper
from deal_scraper.scrapers.amazon import AmazonScraper
from deal_scraper.scrapers.flipkart import FlipkartScraper
from deal_scraper.scrapers.generic import GenericScraper
from deal_scraper.scrapers.myntra import MyntraScraper
from deal_scraper.scrapers.nykaa import NykaaScraper
from deal_scraper.scrapers.snapdeal import SnapdealScraper


def get_scraper(url: str):
    hostname = urlparse(url).netloc.lower()
    if "amazon." in hostname or "amzn.to" in hostname:
        return AmazonScraper()
    if "flipkart." in hostname:
        return FlipkartScraper()
    if "myntra." in hostname:
        return MyntraScraper()
    if "ajio." in hostname:
        return AjioScraper()
    if "nykaa." in hostname:
        return NykaaScraper()
    if "snapdeal." in hostname:
        return SnapdealScraper()
    return GenericScraper()
