from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class SnapdealScraper(BaseScraper):
    site_name = "snapdeal"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        return self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(soup, ["h1.pdp-e-i-head", "h1", "title"]),
                "brand": self.find_text(soup, [".pdp-e-i-brand", ".brand-name"]),
                "price": self.find_text(soup, [".payBlkBig", ".pdp-final-price", ".price"]),
                "image_url": self.find_attr(soup, [".cloudzoom", "img"], "src"),
            },
        )
