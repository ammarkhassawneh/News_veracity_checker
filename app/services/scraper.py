import requests
from bs4 import BeautifulSoup
import logging
from app.config import TRUSTED_SOURCES

# Set up logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def scrape_headlines(url: str) -> list:
    """
    Scrapes headlines from the given news website URL.
    
    Parameters:
        url (str): The URL of the news website.
    
    Returns:
        list: A list of headline strings extracted from h1, h2, and h3 tags.
    """
    headlines = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/88.0.4324.96 Safari/537.36'
    }
    try:
        # Send a GET request with a timeout and custom user-agent header
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return headlines

    # Parse the HTML content using BeautifulSoup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Extract text from h1, h2, and h3 tags as potential headlines
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        text = tag.get_text(strip=True)
        if text:
            headlines.append(text)
    return headlines

def update_trusted_sources() -> dict:
    """
    Scrapes all trusted news sources defined in the configuration and logs their headlines.
    
    In a production scenario, this function might update a reference database with the latest headlines.
    
    Returns:
        dict: A dictionary where keys are source URLs and values are lists of headlines.
    """
    sources_data = {}
    for source in TRUSTED_SOURCES:
        logger.info(f"Scraping headlines from {source}")
        headlines = scrape_headlines(source)
        sources_data[source] = headlines
        logger.info(f"Found {len(headlines)} headlines from {source}")
    return sources_data
