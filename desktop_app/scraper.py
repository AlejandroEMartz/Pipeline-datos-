import requests
from bs4 import BeautifulSoup

def fetch_ticker_data(ticker):
    """
    Realiza el web scraping de un ticker específico en InvertirOnline.
    Retorna un diccionario con los datos o None si falla.
    """
    ticker = ticker.strip().upper()
    url = f"https://iol.invertironline.com/titulo/cotizacion/BCBA/{ticker}/"
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    try:
        response = requests.get(url, headers=headers, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')

            # Buscar Precio
            price_tag = soup.find(attrs={"data-field": "UltimoPrecio"})
            price = price_tag.text.strip() if price_tag else "N/A"

            # Buscar Variación Porcentual
            var_tag = soup.find(attrs={"data-field": "Variacion"})
            variation = var_tag.text.strip() if var_tag else "N/A"

            return {
                "Ticker": ticker,
                "Precio": f"${price}" if price != "N/A" else "N/A",
                "Variacion": f"{variation}%" if variation != "N/A" else "N/A"
            }
        else:
            print(f"Error {response.status_code} al buscar {ticker}")
            return {
                "Ticker": ticker,
                "Precio": "Error",
                "Variacion": "Error"
            }
    except Exception as e:
        print(f"Excepción al buscar {ticker}: {e}")
        return {
            "Ticker": ticker,
            "Precio": "Error",
            "Variacion": "Error"
        }
