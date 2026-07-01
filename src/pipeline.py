import pandas as pd
import logging
import os

class DataPipeline:
    def __init__(self, output_file='data/noticias.csv'):
        self.output_file = output_file

    def process_and_save(self, raw_data):
        """Processes the scraped data and saves it to a CSV."""
        if not raw_data:
            logging.warning("No data provided to the pipeline.")
            return False

        logging.info(f"Processing {len(raw_data)} headlines...")

        # Crear DataFrame
        df = pd.DataFrame(raw_data)

        # Limpiar datos: eliminar espacios extra y saltos de línea dentro de los titulares
        if 'headline' in df.columns:
            df['headline'] = df['headline'].str.replace(r'\s+', ' ', regex=True).str.strip()

            # Filtrar titulares que empiecen con "RECETA DE" (ignorando mayúsculas/minúsculas)
            df = df[~df['headline'].str.contains(r'^receta de\b', case=False, na=False, regex=True)]

        # Eliminar duplicados
        df = df.drop_duplicates(subset=['headline'])

        logging.info(f"Saving {len(df)} unique headlines to {self.output_file}...")

        try:
            # Asegurar que el directorio de salida existe
            os.makedirs(os.path.dirname(self.output_file), exist_ok=True)

            # Guardar a CSV
            df.to_csv(self.output_file, index=False, encoding='utf-8')
            logging.info("Data successfully saved.")
            return True
        except Exception as e:
            logging.error(f"Failed to save data: {e}")
            return False
