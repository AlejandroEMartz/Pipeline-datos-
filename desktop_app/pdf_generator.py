from fpdf import FPDF
from datetime import datetime

class PDFReport(FPDF):
    def header(self):
        # Título
        self.set_font('Arial', 'B', 16)
        self.cell(0, 10, 'Reporte de Mercado - Acciones y Bonos', 0, 1, 'C')

        # Fecha
        self.set_font('Arial', 'I', 10)
        current_date = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        self.cell(0, 10, f'Generado el: {current_date}', 0, 1, 'C')
        self.ln(10)

    def footer(self):
        # Posición a 1.5 cm desde el final
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        # Número de página
        self.cell(0, 10, f'Página {self.page_no()}/{{nb}}', 0, 0, 'C')

def generate_pdf_report(data_list, filename="reporte_mercado.pdf"):
    pdf = PDFReport()
    pdf.alias_nb_pages()
    pdf.add_page()

    # Configurar fuente para la tabla
    pdf.set_font('Arial', 'B', 12)

    # Ancho de las columnas
    col_width = pdf.w / 3.5
    row_height = 10

    # Centrar la tabla (calculamos el margen izquierdo)
    left_margin = (pdf.w - (col_width * 3)) / 2
    pdf.set_left_margin(left_margin)

    # Encabezados de la tabla
    pdf.set_fill_color(200, 220, 255)
    pdf.cell(col_width, row_height, 'Ticker', border=1, align='C', fill=True)
    pdf.cell(col_width, row_height, 'Precio', border=1, align='C', fill=True)
    pdf.cell(col_width, row_height, 'Variación', border=1, align='C', fill=True)
    pdf.ln(row_height)

    # Datos de la tabla
    pdf.set_font('Arial', '', 12)
    for row in data_list:
        pdf.cell(col_width, row_height, row['Ticker'], border=1, align='C')
        pdf.cell(col_width, row_height, row['Precio'], border=1, align='C')
        pdf.cell(col_width, row_height, row['Variacion'], border=1, align='C')
        pdf.ln(row_height)

    pdf.output(filename)
    return filename
