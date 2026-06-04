from __future__ import annotations

import argparse
import json

from deal_scraper.service import scrape_telegram_channel, scrape_url


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="Scrape deals from product URLs or Telegram channels.")
    subparsers = parser.add_subparsers(dest="command", required=True)

    scrape_url_parser = subparsers.add_parser("scrape-url", help="Scrape a single product URL.")
    scrape_url_parser.add_argument("url", help="Product URL to scrape.")

    scrape_channel_parser = subparsers.add_parser(
        "scrape-channel",
        help="Scrape recent Telegram messages and resolve product links.",
    )
    scrape_channel_parser.add_argument("--channel", required=True, help="Telegram channel username.")
    scrape_channel_parser.add_argument("--limit", type=int, default=10, help="Number of messages to read.")

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "scrape-url":
        result = scrape_url(args.url)
    elif args.command == "scrape-channel":
        result = scrape_telegram_channel(channel=args.channel, limit=args.limit)
    else:
        parser.error(f"Unsupported command: {args.command}")
        return

    print(json.dumps(result, indent=2, ensure_ascii=True))


if __name__ == "__main__":
    main()
