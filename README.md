# Pipeline de Web Scraping - Noticias de Argentina

Este repositorio contiene un pipeline de datos desarrollado en Python para extraer titulares de los 15 principales medios de noticias de Argentina, procesarlos y guardarlos en un formato estructurado (CSV).

## Características

- Extrae titulares (etiquetas `<h2>` y `<h3>`) de múltiples sitios de noticias.
- Procesa la información eliminando saltos de línea y textos duplicados.
- Consolida todos los titulares scrapeados en el archivo `data/noticias.csv`.
- Maneja excepciones por fallos de conexión o tiempos de espera agotados para no interrumpir el flujo.

## Medios Incluidos

Infobae, La Nación, Clarín, TN, Página/12, Perfil, Ámbito Financiero, El Cronista, Minuto Uno, C5N, La Voz (Córdoba), Los Andes (Mendoza), El Destape, MDZ Online y Rosario 3.

## Instalación

Es recomendable usar un entorno virtual para instalar las dependencias.

```bash
# Instalar los requerimientos necesarios
pip install -r requirements.txt
```

## Uso

Para ejecutar el pipeline completo de extracción y procesamiento:

```bash
python main.py
```

El script buscará las fuentes de `src/config.py`, extraerá los datos utilizando `src/scraper.py`, los limpiará a través de `src/pipeline.py` y finalmente generará el archivo `data/noticias.csv`.
