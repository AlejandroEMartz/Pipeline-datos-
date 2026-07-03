import os
import csv
from datetime import datetime
import feedparser
from twilio.rest import Client

def get_news():
    # URL de ejemplo de noticias RSS (BBC Mundo)
    feed_url = 'https://feeds.bbci.co.uk/mundo/rss.xml'
    feed = feedparser.parse(feed_url)

    noticias = []
    # Obtener el top 5 de noticias
    for entry in feed.entries[:5]:
        # Para evitar errores con atributos faltantes
        published = getattr(entry, 'published', datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        noticias.append({
            'title': entry.title,
            'link': entry.link,
            'published': published
        })
    return noticias

def save_to_spreadsheet(noticias, filename):
    file_exists = os.path.isfile(filename)

    with open(filename, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(file, fieldnames=['title', 'link', 'published'])

        if not file_exists:
            writer.writeheader()

        for noticia in noticias:
            writer.writerow(noticia)

def send_whatsapp_summary(noticias):
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM')
    to_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_TO')

    if not all([account_sid, auth_token, from_whatsapp_number, to_whatsapp_number]):
        print("Faltan credenciales de Twilio. Saltando el envío por WhatsApp.")
        return

    client = Client(account_sid, auth_token)

    today_str = datetime.now().strftime("%Y-%m-%d")
    summary = f"Resumen de Noticias - {today_str}\n\n"

    for i, noticia in enumerate(noticias, 1):
        summary += f"{i}. {noticia['title']}\n"

    summary += "\nRevisa tu spreadsheet local para más detalles."

    message = client.messages.create(
        body=summary,
        from_=from_whatsapp_number,
        to=to_whatsapp_number
    )
    print(f"Mensaje de WhatsApp enviado con SID: {message.sid}")

def main():
    print("Obteniendo noticias...")
    noticias = get_news()

    if not noticias:
        print("No se encontraron noticias. Saliendo.")
        return

    # Crear un spreadsheet con las noticias de cada día
    today_str = datetime.now().strftime("%Y-%m-%d")
    spreadsheet_filename = f"noticias_{today_str}.csv"

    print(f"Guardando en el spreadsheet: {spreadsheet_filename}...")
    save_to_spreadsheet(noticias, spreadsheet_filename)

    print("Enviando resumen por WhatsApp...")
    send_whatsapp_summary(noticias)
    print("Pipeline de datos ejecutado con éxito.")

if __name__ == "__main__":
    main()
