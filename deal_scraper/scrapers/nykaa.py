from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class NykaaScraper(BaseScraper):
    site_name = "nykaa"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        return self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(soup, ["h1", ".css-175dy2r", "title"]),
                "brand": self.find_text(soup, [".css-xrzmfa", ".product-brand-name"]),
                "price": self.find_text(soup, [".css-111z9ua", ".css-14b29qc", ".price"]),
                "image_url": self.find_attr(soup, ["img.css-1gc4x7i", "img"], "src"),
            },
        )
