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
    
    This function uses BeautifulSoup to extract text from header tags (h1, h2, h3)
    to gather potential news headlines.
    
    Parameters:
        url (str): The URL of the news website.
    
    Returns:
        list: A list of headline strings extracted from the page.
    """
    headlines = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                      '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching URL {url}: {e}")
        return headlines

    soup = BeautifulSoup(response.text, 'html.parser')
    for tag in soup.find_all(['h1', 'h2', 'h3']):
        text = tag.get_text(strip=True)
        if text:
            headlines.append(text)
    return headlines

def update_trusted_sources() -> dict:
    """
    Scrapes headlines from all trusted news sources defined in the configuration.
    
    This function iterates through the list of trusted sources (e.g., BBC, CNN, Reuters, etc.),
    scrapes their headlines, and logs the number of headlines found for each source.
    
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

def search_google_news(keyword: str) -> list:
    """
    Searches Google News for the given keyword and extracts headlines from the search results.
    
    This function builds a Google News search URL based on the keyword, fetches the page,
    and uses BeautifulSoup to extract headlines. Note that the structure of the Google News
    results page may change over time, so adjustments might be needed.
    
    Parameters:
        keyword (str): The search keyword to look for in Google News.
    
    Returns:
        list: A list of headlines retrieved from the Google News search results.
    """
    headlines = []
    url = f"https://news.google.com/search?q={keyword}"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ' \
                      '(KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36'
    }
    try:
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
    except requests.RequestException as e:
        logger.error(f"Error fetching Google News for keyword '{keyword}': {e}")
        return headlines
    
    soup = BeautifulSoup(response.text, 'html.parser')
    # Extract headlines from anchor tags. This may need to be adjusted based on the current HTML structure.
    for a in soup.find_all('a'):
        text = a.get_text(strip=True)
        if text and len(text) > 10:  # Simple filter to avoid very short texts
            headlines.append(text)
    return headlines
