from __future__ import annotations

from deal_scraper.scrapers.base import BaseScraper


class AmazonScraper(BaseScraper):
    site_name = "amazon"

    def scrape(self, url: str):
        response, soup = self.fetch(url)
        product = self.build_product(
            source_url=url,
            response=response,
            soup=soup,
            overrides={
                "title": self.find_text(soup, ["#productTitle", "h1 span", "title"]),
                "brand": self.find_text(soup, ["#bylineInfo", "#productOverview_feature_div td"]),
                "price": self.find_text(
                    soup,
                    [
                        ".a-price .a-offscreen",
                        "#corePriceDisplay_desktop_feature_div .a-offscreen",
                        "#tp_price_block_total_price_ww .a-offscreen",
                    ],
                ),
                "image_url": (
                    soup.select_one("#landingImage").get("src")
                    if soup.select_one("#landingImage")
                    else None
                ),
                "availability": self.find_text(soup, ["#availability span"]),
                "rating": self.find_text(soup, ["#acrPopover", ".a-icon-alt"]),
            },
        )
        return product
