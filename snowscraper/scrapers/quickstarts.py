from datetime import datetime
from datetime import timezone

import scrapy
from scrapy import signals
from scrapy.crawler import CrawlerProcess
from scrapy.signalmanager import dispatcher

from ..controller import register_scraper
from ..scraper import BaseScraper
from snowscraper.helpers import string_to_datetime

QuickStartsURL = "https://quickstarts.snowflake.com/"


@register_scraper
class QuickstartScraper(BaseScraper, scrapy.Spider):
    name = "snowflakespider"

    def __init__(self, *args, **kwargs):
        super(QuickstartScraper, self).__init__(*args, **kwargs)
        self.data = {}
        self.after = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def start_requests(self):
        yield scrapy.Request(url=QuickStartsURL, callback=self.parse)

    def signal_handler(self, signal, sender, item, response, spider):
        self.data[item["key"]] = item
        self.data[item["key"]].pop("key")

    def scrape(self):
        print("Scraping Quickstarts")
        dispatcher.connect(self.signal_handler, signal=signals.item_scraped)
        process = CrawlerProcess({"LOG_LEVEL": "ERROR"})
        process.crawl(QuickstartScraper, after=self.after)
        process.start()
        return self.data

    def parse(self, response):
        for card in response.css("card-sorter#cards > a.codelab-card"):
            updated = string_to_datetime(card.attrib["data-updated"])
            if updated > self.after:
                key = QuickStartsURL.rstrip("/") + card.attrib["href"]
                yield {
                    "key": key,
                    "title": card.attrib["data-title"],
                    "updated": updated,
                    "tags": card.attrib["data-tags"],
                }

    def transform(self):
        return self.data
