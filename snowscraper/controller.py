import json
import argparse
import importlib
import pkgutil
from pathlib import Path

SCRAPERS = {}

def register_scraper(cls):
    SCRAPERS[cls.__name__] = cls
    return cls

def run_all(args: argparse.Namespace):
    results = {}
    for scraper_cls in SCRAPERS.values():
        scraper = scraper_cls()
        results.update(scraper.scrape())
    print(results)

    # Save the results to a JSON file
    with open('results.json', 'w') as json_file:
        json.dump(results, json_file, indent=4, default=datetime_handler)

def datetime_handler(obj):
    if isinstance(obj, datetime.datetime):
        return obj.isoformat()
    raise TypeError("Unknown type")

def import_scrapers():
    directory = Path(__file__).resolve().parent / "scrapers"
    for module_loader, name, ispkg in pkgutil.iter_modules([directory]):
        importlib.import_module(f".scrapers.{name}", __package__)
