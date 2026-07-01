import logging
from src.scraper import NewsScraper
from src.pipeline import DataPipeline
from src.config import NEWS_SOURCES

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    logging.info("Starting Argentine News Pipeline...")

    scraper = NewsScraper()
    pipeline = DataPipeline()

    all_headlines = []

    # Iterar sobre las fuentes y extraer datos
    for source in NEWS_SOURCES:
        try:
            headlines = scraper.scrape(source['url'], source['name'])
            if headlines:
                all_headlines.extend(headlines)
        except Exception as e:
            logging.error(f"Failed to process {source['name']}: {e}")
            continue

    # Procesar y guardar todos los datos juntos
    if all_headlines:
        logging.info(f"Total headlines scraped: {len(all_headlines)}")
        pipeline.process_and_save(all_headlines)
    else:
        logging.warning("No headlines were scraped from any source.")

    logging.info("Pipeline finished.")

if __name__ == "__main__":
    main()
