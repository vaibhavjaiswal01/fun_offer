from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class FlipkartScraper(BaseScraper):
    site_name = "flipkart"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        product = self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(soup, ["span.B_NuCI", "h1", "title"]),
                "brand": self.find_text(soup, ["span.G6XhRU", "a._2whKao", ".mEh187"]),
                "price": self.find_text(soup, ["div._30jeq3", "div.Nx9bqj", "._16Jk6d"]),
                "image_url": (
                    soup.select_one("img._396cs4").get("src")
                    if soup.select_one("img._396cs4")
                    else None
                ),
                "availability": self.find_text(soup, ["div._16FRp0", "div.Z8JjpR"]),
                "rating": self.find_text(soup, ["div._3LWZlK", "div.XQDdHH"]),
            },
        )
        return product
