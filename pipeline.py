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

def analyze_spreadsheet_and_send_whatsapp(filename):
    if not os.path.isfile(filename):
        print(f"El archivo {filename} no existe para analizar.")
        return

    # 1. Leer el archivo CSV generado ("archivo de data")
    noticias_leidas = []
    with open(filename, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            noticias_leidas.append(row)

    if not noticias_leidas:
        print("El archivo CSV está vacío.")
        return

    # 2. Configurar credenciales
    account_sid = os.environ.get('TWILIO_ACCOUNT_SID')
    auth_token = os.environ.get('TWILIO_AUTH_TOKEN')
    from_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_FROM')
    to_whatsapp_number = os.environ.get('TWILIO_WHATSAPP_TO')

    # 3. Realizar un análisis/resumen basado en los datos extraídos del CSV
    today_str = datetime.now().strftime("%Y-%m-%d")
    total_noticias = len(noticias_leidas)

    summary = f"📊 Análisis del archivo de datos ({today_str})\n"
    summary += f"Total de noticias procesadas: {total_noticias}\n\n"
    summary += "📰 Últimos titulares:\n"

    # Mostramos los últimos 5 del archivo para el resumen del análisis
    for i, noticia in enumerate(noticias_leidas[-5:], 1):
        summary += f"• {noticia['title']}\n"

    summary += f"\n📁 Datos leídos de: {filename}"

    # 4. Enviar por WhatsApp
    if not all([account_sid, auth_token, from_whatsapp_number, to_whatsapp_number]):
        print("Faltan credenciales de Twilio. Se muestra el análisis por consola pero no se envía por WhatsApp.")
        print("\n--- RESUMEN A ENVIAR (Simulado) ---")
        print(summary)
        print("-----------------------------------\n")
    else:
        client = Client(account_sid, auth_token)
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

    print("Leyendo el archivo de data generado y creando el resumen para WhatsApp...")
    analyze_spreadsheet_and_send_whatsapp(spreadsheet_filename)
    print("Pipeline de datos ejecutado con éxito.")

if __name__ == "__main__":
    main()
