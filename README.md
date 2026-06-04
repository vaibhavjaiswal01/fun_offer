# Deal Scraper

A production-ready Python project for collecting deal links from Telegram and scraping product metadata from common Indian e-commerce sites such as Amazon, Flipkart, and Myntra.

## Features

- Clean project structure with reusable scraper modules
- Site-aware scrapers for Amazon, Flipkart, Myntra, Ajio, Nykaa, and Snapdeal
- Generic scraper fallback for other product pages
- Telegram channel ingestion using `Telethon`
- CLI entrypoint with `main.py`
- Flask API server with `app.py`
- Docker support
- Environment-based configuration

## Project Structure

```text
deal_scraper/
  scrapers/
    __init__.py
    amazon.py
    base.py
    flipkart.py
    generic.py
    myntra.py
    router.py
  __init__.py
  config.py
  models.py
  service.py
  telegram_client.py
app.py
main.py
requirements.txt
Dockerfile
.env.example
```

## Supported Sites

- Amazon
- Flipkart
- Myntra
- Ajio
- Nykaa
- Snapdeal
- Generic product pages that expose Open Graph or JSON-LD product metadata

## Quick Start

### 1. Create a virtual environment

```bash
python -m venv .venv
source .venv/bin/activate
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure environment

```bash
cp .env.example .env
```

Fill in your Telegram credentials in `.env` if you want to fetch deals from Telegram.

## Usage

### Scrape a single product URL

```bash
python main.py scrape-url "https://www.amazon.in/dp/B0..."
```

### Scrape recent messages from a Telegram channel

```bash
python main.py scrape-channel --channel nonstopdeals --limit 10
```

### Run the API server

```bash
python app.py
```

Server endpoints:

- `GET /health`
- `POST /scrape`
- `POST /telegram/scrape`

## Example API Requests

### Scrape one URL

```bash
curl -X POST http://127.0.0.1:5000/scrape \
  -H "Content-Type: application/json" \
  -d '{"url":"https://www.flipkart.com/..."}'
```

### Scrape deals from Telegram

```bash
curl -X POST http://127.0.0.1:5000/telegram/scrape \
  -H "Content-Type: application/json" \
  -d '{"channel":"nonstopdeals","limit":5}'
```

## Docker

Build:

```bash
docker build -t deal-scraper .
```

Run:

```bash
docker run --env-file .env -p 5000:5000 deal-scraper
```

## Notes

- Some sites change markup frequently, so scraper rules may need periodic updates.
- Many e-commerce sites use bot protection. This project uses polite headers and metadata-first extraction, but scraping success can still vary.
- Never commit your Telegram API credentials to the repository.
