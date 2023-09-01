from abc import ABC
from abc import abstractmethod


class BaseScraper(ABC):
    def run(self, validate=True):
        self.scraped_json = self._scrape()
        self.transformed_json = self._transform(self.scraped_json)
        if validate:
            self.validate()
        return self.transformed_json

    def validate(self):
        if not self.transformed_json:
            return self.transformed_json

    @abstractmethod
    def scrape(self):
        pass

    @abstractmethod
    def transform(self):
        pass
