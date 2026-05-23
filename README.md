# Watch‑Notify

A **tiny** cross‑platform Python script that watches a directory and posts a message to a webhook (Discord, Slack, Mattermost, etc.) whenever a new file appears.

## Features
- Zero‑dependency runtime besides `watchdog` and `requests`.
- Configurable via CLI flags or environment variables.
- Debounce logic to avoid spamming the webhook when many files arrive at once.
- Works on Windows, macOS and Linux.

## Quick Start
```bash
# Clone the repo
git clone https://github.com/yourname/watch-notify.git
cd watch-notify

# Install dependencies (prefer a venv)
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

# Run the watcher (replace <WEBHOOK_URL> with your Discord/Slack webhook)
python watch_notify.py --path ./incoming --webhook <WEBHOOK_URL>
```

You can also set the environment variable `DISCORD_WEBHOOK` (or any name you prefer) instead of passing `--webhook`.

## Usage
```
python watch_notify.py 
    --path ./incoming               # Directory to monitor (required)
    --webhook https://...           # Webhook URL (optional, env var fallback)
    --debounce 2.0                  # Minimum seconds between notifications (default 2s)
```

## Development
Run the test suite with:
```bash
pytest
```

The GitHub Actions workflow (see `.github/workflows/ci.yml`) runs `flake8` linting and the pytest suite on every push.

## License
MIT – see the `LICENSE` file.
