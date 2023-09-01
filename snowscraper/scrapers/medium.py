from datetime import datetime
from datetime import timezone

import feedparser

from ..controller import register_scraper
from ..helpers import string_to_datetime
from ..scraper import BaseScraper


@register_scraper
class MediumScraper(BaseScraper):
    url = "https://medium.com/feed/snowflake"

    def __init__(self, *args, **kwargs):
        super(MediumScraper, self).__init__(*args, **kwargs)
        self.data = {}
        self.after = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def scrape(self):
        print("Scraping Medium")
        for entry in feedparser.parse(MediumScraper.url)["entries"]:
            updated = string_to_datetime(entry["updated"])
            if updated > self.after:
                self.data[entry["link"]] = {
                    "title": entry["title"],
                    "published": string_to_datetime(entry["published"]),
                    "updated": updated,
                }
        return self.data

    def transform(self):
        return self.data
