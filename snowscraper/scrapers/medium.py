from datetime import datetime
from datetime import timezone

import requests

from ..controller import register_scraper
from ..helpers import unix_to_datetime_utc
from ..scraper import BaseScraper


LONG_QUERY = """
query PublicationHomepageQuery($collectionId: ID!, $homepagePostsLimit: PaginationLimit = 25, $homepagePostsFrom: String, $includeDistributedResponses: Boolean = false) {
  collection(id: $collectionId) {
      homepagePostsConnection(
      paging: {limit: $homepagePostsLimit, from: $homepagePostsFrom}
      includeDistributedResponses: $includeDistributedResponses
    ) {
      posts {
          firstPublishedAt
          latestPublishedAt
          title
          uniqueSlug
          visibility
          mediumUrl
          isPublished
          tags {
            normalizedTagSlug
          }
      }
      pagingInfo {
        next {
          from
          limit
        }
      }
    }
  }
}
"""

@register_scraper
class MediumScraper(BaseScraper):
    url = "https://medium.com/_/graphql"

    def __init__(self, *args, **kwargs):
        super(MediumScraper, self).__init__(*args, **kwargs)
        self.data = {}
        self.after = datetime(1970, 1, 1, tzinfo=timezone.utc)

    def make_request(self, query_vars):
        response = requests.post(self.url, json=query_vars)
        post_data = response.json()["data"]["collection"]["homepagePostsConnection"]
        paging_info = post_data['pagingInfo']
        return post_data["posts"], paging_info

    def scrape(self):
        print("Scraping Medium")
        query_vars = {
            "query": LONG_QUERY,
            "variables": {
                "homepagePostsLimit": 25,
                "includeDistributedResponses": False,
                "collectionId": "34b6daafc07",
                "homepagePostsFrom": "0"
            }
        }
        
        while True:
            posts, paging_info = self.make_request(query_vars)
            
            for post in posts:
                if post["visibility"] == "PUBLIC" and post["isPublished"]:
                    self.data[post["mediumUrl"]] = {
                        "title": post["title"],
                        "published": unix_to_datetime_utc(post["firstPublishedAt"]),
                        "updated": unix_to_datetime_utc(post["latestPublishedAt"]),
                        "tags": ",".join(tag["normalizedTagSlug"] for tag in post["tags"])
                    }
                    
            if paging_info is None:
                break

            query_vars['variables']['homepagePostsFrom'] = paging_info['next']['from']
            query_vars['variables']['homepagePostsLimit'] = paging_info['next']['limit']
        
        return self.data

    def transform(self):
        return self.data
