#!/usr/bin/env python3
"""watch_notify.py
A tiny script that watches a directory for new files and posts a notification to a webhook.

Author: TopherBot <topherbot@proton.me>
"""

import argparse
import json
import logging
import os
import pathlib
import sys
import time
from typing import Optional

import requests
from watchdog.events import FileSystemEventHandler
from watchdog.observers import Observer

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(message)s",
)


class NotifyHandler(FileSystemEventHandler):
    """Handle created‑file events and send a webhook notification."""

    def __init__(self, webhook_url: str, debounce: float):
        self.webhook_url = webhook_url
        self.debounce = debounce
        self.last_sent = 0.0

    def on_created(self, event):
        if event.is_directory:
            return
        now = time.time()
        if now - self.last_sent < self.debounce:
            # Skip rapid successive events
            return
        self.last_sent = now
        filename = pathlib.Path(event.src_path).name
        payload = {"content": f":incoming_envelope: New file detected: `{filename}`"}
        try:
            resp = requests.post(self.webhook_url, json=payload, timeout=5)
            resp.raise_for_status()
            logging.info("Notification sent for %s", filename)
        except Exception as exc:
            logging.error("Failed to send notification: %s", exc)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Watch a directory and send webhook notifications on new files."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="Directory to watch (must exist).",
    )
    parser.add_argument(
        "--webhook",
        required=False,
        help="Webhook URL; if omitted, DISCORD_WEBHOOK env var will be used.",
    )
    parser.add_argument(
        "--debounce",
        type=float,
        default=2.0,
        help="Minimum seconds between notifications (default: 2.0).",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    webhook: Optional[str] = args.webhook or os.getenv("DISCORD_WEBHOOK")
    if not webhook:
        logging.error(
            "Webhook URL not provided. Use --webhook or set DISCORD_WEBHOOK environment variable."
        )
        sys.exit(1)

    watch_path = pathlib.Path(args.path).resolve()
    if not watch_path.is_dir():
        logging.error("The path %s is not a directory.", watch_path)
        sys.exit(1)

    handler = NotifyHandler(webhook, args.debounce)
    observer = Observer()
    observer.schedule(handler, str(watch_path), recursive=False)
    observer.start()
    logging.info("Watching %s for new files...", watch_path)
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        logging.info("Interrupted – stopping watcher.")
        observer.stop()
    observer.join()


if __name__ == "__main__":
    main()
