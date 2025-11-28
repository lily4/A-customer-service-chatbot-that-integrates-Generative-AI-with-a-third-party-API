import requests

BASE_URL = "https://zenquotes.io/api/random"

def get_random_quote(tag: str | None = None) -> dict:
    """
    Get a random quote from ZenQuotes API.
    The tag parameter is kept for compatibility but not used by ZenQuotes.
    Returns a dict with 'content' and 'author' keys.
    """
    response = requests.get(BASE_URL, timeout=5)
    response.raise_for_status()
    data = response.json()

    if isinstance(data, list) and data:
        quote_data = data[0]
        return {
            "content": quote_data.get("q", ""),
            "author": quote_data.get("a", "Unknown"),
        }

    return {
        "content": "Keep going. Your creativity matters.",
        "author": "Unknown",
    }
