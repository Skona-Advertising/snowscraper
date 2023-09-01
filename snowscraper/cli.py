import argparse
import sys
from datetime import datetime
from datetime import timezone

from .controller import import_scrapers
from .controller import run_all


def main(args: argparse.Namespace) -> None:
    import_scrapers()
    run_all(args)


def run():
    parser = argparse.ArgumentParser(description="Snowflake scraper")
    parser.add_argument(
        "--after",
        type=str,
        required=False,
        default=None,
        help="Scrape only after a specific date in the format 'MM-DD-YYYY' in UTC",
    )

    args = parser.parse_args()

    if args.after:
        try:
            args.after = datetime.strptime(args.after, "%m-%d-%Y").replace(tzinfo=timezone.utc)
        except ValueError:
            print(f"Error: The 'after' argument should be in the format MM-DD-YYYY. You provided: {args.after}")
            sys.exit(1)
    main(args)


if __name__ == "__main__":
    run()
