from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class GenericScraper(BaseScraper):
    site_name = "generic"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        title = self.find_text(soup, ["h1", "title"])
        description = self.find_attr(
            soup,
            [
                'meta[name="description"]',
                'meta[property="og:description"]',
            ],
            "content",
        )
        if not description:
            description = self.find_text(soup, [".product-description", ".description", "p"])
        image_url = self.find_attr(
            soup,
            ['meta[property="og:image"]', 'meta[name="twitter:image"]', "img"],
            "content",
        )
        if not image_url:
            image_url = self.find_attr(soup, ["img"], "src")
        return self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={"title": title, "description": description, "image_url": image_url},
        )
