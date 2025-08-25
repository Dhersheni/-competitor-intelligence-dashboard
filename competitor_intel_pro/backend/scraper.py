# backend/scraper.py

import requests
from bs4 import BeautifulSoup


def fetch_website_update(url):
    """
    Fetches the latest update from a competitor's website.
    Currently returns the first <h1> or <title> as a placeholder.
    """
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # Example: pick first <h1> text, fallback to <title>
        h1 = soup.find("h1")
        if h1 and h1.text.strip():
            return h1.text.strip()
        title = soup.find("title")
        return title.text.strip() if title else "No update found"
    except Exception as e:
        return f"Failed to fetch website: {e}"
