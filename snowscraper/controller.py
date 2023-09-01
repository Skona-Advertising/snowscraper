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
        scraper = scraper_cls(after=args.after)
        results |= scraper.scrape()
    print(results)


def import_scrapers():
    directory = Path(__file__).resolve().parent / "scrapers"
    for module_loader, name, ispkg in pkgutil.iter_modules([directory]):
        importlib.import_module(f".scrapers.{name}", __package__)
