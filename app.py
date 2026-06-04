from __future__ import annotations

from flask import Flask, jsonify, request

from deal_scraper.config import settings
from deal_scraper.service import scrape_telegram_channel, scrape_url

app = Flask(__name__)


@app.get("/health")
def health():
    return jsonify({"status": "ok"})


@app.post("/scrape")
def scrape_single_url():
    payload = request.get_json(silent=True) or {}
    url = payload.get("url") or request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' in JSON body or query string."}), 400
    try:
        return jsonify(scrape_url(url))
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc), "url": url}), 500


@app.post("/telegram/scrape")
def scrape_from_telegram():
    payload = request.get_json(silent=True) or {}
    channel = payload.get("channel") or request.args.get("channel")
    limit = int(payload.get("limit") or request.args.get("limit") or 10)
    if not channel:
        return jsonify({"error": "Missing 'channel' in JSON body or query string."}), 400
    try:
        return jsonify(scrape_telegram_channel(channel=channel, limit=limit))
    except Exception as exc:  # noqa: BLE001
        return jsonify({"error": str(exc), "channel": channel}), 500


if __name__ == "__main__":
    app.run(host=settings.flask_host, port=settings.flask_port)
