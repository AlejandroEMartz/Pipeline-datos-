import customtkinter as ctk
import threading
import os
from scraper import fetch_ticker_data
from pdf_generator import generate_pdf_report

# Configuración básica de CustomTkinter
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue")

class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        # Configuración de la ventana principal
        self.title("Generador de Reportes - Acciones y Bonos (IOL)")
        self.geometry("500x400")
        self.resizable(False, False)

        # Título
        self.title_label = ctk.CTkLabel(
            self, text="Reporte de Mercado (IOL)", font=ctk.CTkFont(size=20, weight="bold")
        )
        self.title_label.pack(pady=(20, 10))

        # Instrucciones
        self.instructions_label = ctk.CTkLabel(
            self, text="Ingrese los Tickers separados por comas (Ej: AL30, GGAL, YPFD):"
        )
        self.instructions_label.pack(pady=(10, 5))

        # Campo de entrada (Entry) para los Tickers
        self.tickers_entry = ctk.CTkEntry(
            self, width=300, placeholder_text="Ej: AL30, YPFD, BMA"
        )
        self.tickers_entry.pack(pady=10)

        # Botón para generar el reporte
        self.generate_btn = ctk.CTkButton(
            self, text="Generar Reporte en PDF", command=self.start_generation_thread
        )
        self.generate_btn.pack(pady=20)

        # Barra de progreso (indeterminada mientras carga)
        self.progress_bar = ctk.CTkProgressBar(self, width=300)
        self.progress_bar.pack(pady=5)
        self.progress_bar.set(0)
        self.progress_bar.pack_forget() # Ocultar inicialmente

        # Etiqueta de estado
        self.status_label = ctk.CTkLabel(self, text="", text_color="gray")
        self.status_label.pack(pady=10)

    def start_generation_thread(self):
        tickers_input = self.tickers_entry.get()
        if not tickers_input.strip():
            self.status_label.configure(text="Por favor, ingrese al menos un Ticker.", text_color="red")
            return

        # Deshabilitar botón y mostrar progreso
        self.generate_btn.configure(state="disabled")
        self.progress_bar.pack(pady=5)
        self.progress_bar.start()
        self.status_label.configure(text="Iniciando scraping...", text_color="blue")

        # Ejecutar en un hilo separado para no congelar la UI
        threading.Thread(target=self.process_report, args=(tickers_input,)).start()

    def process_report(self, tickers_input):
        tickers = [t.strip() for t in tickers_input.split(',')]
        data_list = []

        for i, ticker in enumerate(tickers):
            if not ticker:
                continue

            self.update_status(f"Buscando datos de {ticker} ({i+1}/{len(tickers)})...", "blue")
            data = fetch_ticker_data(ticker)
            data_list.append(data)

        if data_list:
            self.update_status("Generando archivo PDF...", "blue")
            try:
                filename = "reporte_mercado.pdf"
                filepath = os.path.join(os.getcwd(), filename)
                generate_pdf_report(data_list, filepath)
                self.update_status(f"¡Éxito! PDF guardado en:\n{filepath}", "green")
            except Exception as e:
                self.update_status(f"Error al generar PDF: {e}", "red")
        else:
            self.update_status("No se encontraron datos para los tickers ingresados.", "red")

        # Restaurar UI
        self.after(0, self.restore_ui)

    def update_status(self, message, color):
        # Actualizar etiqueta de forma segura desde el hilo
        self.after(0, lambda: self.status_label.configure(text=message, text_color=color))

    def restore_ui(self):
        self.progress_bar.stop()
        self.progress_bar.pack_forget()
        self.generate_btn.configure(state="normal")

if __name__ == "__main__":
    app = App()
    app.mainloop()
