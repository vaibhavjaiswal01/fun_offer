from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class AjioScraper(BaseScraper):
    site_name = "ajio"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        return self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(soup, [".prod-name", ".product-title", "h1", "title"]),
                "brand": self.find_text(soup, [".brand-name", ".prod-brand", ".brand"]),
                "price": self.find_text(soup, [".price .amount", ".prod-sp", ".price"]),
                "image_url": self.find_attr(soup, [".imgHolder img", ".prod-image img", "img"], "src"),
            },
        )
