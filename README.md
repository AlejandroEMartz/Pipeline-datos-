# Pipeline-datos-
Pipeline de automatización diaria de noticias y envío de resúmenes por WhatsApp.

## Descripción

Este proyecto extrae automáticamente las noticias más relevantes cada día mediante fuentes RSS, las guarda localmente en formato de tabla (CSV/Spreadsheet) para llevar un registro y envía un mensaje de resumen a un número de WhatsApp a través de la API de Twilio. Está optimizado y automatizado con GitHub Actions para funcionar en segundo plano sin intervención manual.

## Funcionamiento

- **pipeline.py**: El script principal que se encarga de la extracción de noticias, la generación del archivo CSV de cada día y el envío del mensaje por WhatsApp.
- **GitHub Actions**: Cada día (a las 12:00 PM UTC por defecto), un flujo de trabajo de GitHub Action (`daily.yml`) ejecuta el script y guarda el CSV del día como un "Artifact" que puedes descargar desde la pestaña "Actions" del repositorio.

## Configuración

Para que el envío de WhatsApp funcione, necesitas crear una cuenta gratuita en [Twilio](https://www.twilio.com/) y habilitar el **Twilio Sandbox for WhatsApp**.

Una vez hecho esto, configura los siguientes "Secrets" en tu repositorio de GitHub (en `Settings` -> `Secrets and variables` -> `Actions` -> `New repository secret`):

- `TWILIO_ACCOUNT_SID`: El SID de tu cuenta de Twilio.
- `TWILIO_AUTH_TOKEN`: El token de autenticación de tu cuenta de Twilio.
- `TWILIO_WHATSAPP_FROM`: El número del sandbox de Twilio (formato `whatsapp:+14155238886`).
- `TWILIO_WHATSAPP_TO`: Tu número de teléfono para recibir el mensaje (formato `whatsapp:+TUNUMERO`).

Si ejecutas el código localmente, estas variables también deben estar configuradas como variables de entorno.

## Ejecución Local

Para probarlo localmente:

1. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
2. Ejecuta el script:
   ```bash
   python pipeline.py
   ```
