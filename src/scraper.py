import requests
from bs4 import BeautifulSoup
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class NewsScraper:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept-Language': 'es-ES,es;q=0.9',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'
        }

    def fetch_html(self, url):
        """Fetches the HTML content of a given URL."""
        try:
            response = requests.get(url, headers=self.headers, timeout=15)
            response.raise_for_status()
            return response.text
        except requests.RequestException as e:
            logging.error(f"Error fetching {url}: {e}")
            return None

    def parse_headlines(self, html, source_name):
        """Parses the HTML to extract headlines from h2 and h3 tags."""
        headlines = []
        if not html:
            return headlines

        soup = BeautifulSoup(html, 'html.parser')

        # Encontrar todas las etiquetas h2 y h3
        tags = soup.find_all(['h2', 'h3'])

        for tag in tags:
            text = tag.get_text(strip=True)
            if text and len(text) > 10:  # Filtrar textos muy cortos que no suelen ser noticias
                headlines.append({
                    'source': source_name,
                    'headline': text
                })

        return headlines

    def scrape(self, url, source_name):
        """Orchestrates the scraping process for a single URL."""
        logging.info(f"Scraping {source_name} ({url})...")
        html = self.fetch_html(url)
        return self.parse_headlines(html, source_name)
