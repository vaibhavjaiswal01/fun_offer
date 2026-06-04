from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class MyntraScraper(BaseScraper):
    site_name = "myntra"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        product = self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(
                    soup,
                    [
                        "h1.pdp-title",
                        "h1.pdp-name",
                        "h1",
                        "title",
                    ],
                ),
                "brand": self.find_text(soup, ["h1.pdp-title", ".pdp-title"]),
                "price": self.find_text(soup, ["span.pdp-price strong", ".pdp-price strong"]),
                "image_url": (
                    soup.select_one("img.image-base-img").get("src")
                    if soup.select_one("img.image-base-img")
                    else None
                ),
                "availability": self.find_text(soup, [".pdp-add-to-bag", ".size-buttons-size-button"]),
                "rating": self.find_text(soup, [".index-overallRating", ".pdp-review-stars"]),
            },
        )
        return product
