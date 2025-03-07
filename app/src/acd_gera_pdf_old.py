from django.http import HttpResponse
import pandas as pd
import csv
import io

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter, A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, PageTemplate, Frame
from reportlab.platypus import BaseDocTemplate
from reportlab.lib import colors
from reportlab.platypus.flowables import PageBreak
from reportlab.lib.styles import getSampleStyleSheet


def gerarPDF_old(valores, headers, df):
        
    if valores[4] == "1":
		
        pdf_path = "relatorio.pdf"
        
		# Configuração básica do documento
        if len(headers) <= 4:
            tam_pagina = A4
        else:
            tam_pagina = landscape(A4)        
        pdf_doc = SimpleDocTemplate(pdf_path, pagesize=tam_pagina)
                    
        elements = []

		# Dados para o PDF (incluindo cabeçalho)
        table_data = [headers] + df.values.tolist()

		# Estilizando a tabela
        table = Table(table_data)
        table.setStyle(TableStyle([
			('BACKGROUND', (0, 0), (-1, 0), colors.grey),  # Fundo do cabeçalho
			('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  # Cor do texto do cabeçalho
			('ALIGN', (0, 0), (-1, -1), 'CENTER'),  # Alinhamento central
			('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),  # Fonte do cabeçalho
			('BOTTOMPADDING', (0, 0), (-1, 0), 12),  # Padding do cabeçalho
			('BACKGROUND', (0, 1), (-1, -1), colors.beige),  # Fundo das linhas
			('GRID', (0, 0), (-1, -1), 1, colors.black)  # Grade da tabela
		]))

        elements.append(table)

        #if len(df) > 20:  # Ajuste o número de linhas conforme necessário
        #    elements.append(PageBreak())  # Cria uma quebra de página
        
		# Construção do documento
        pdf_doc.build(elements)
        nome_tabela = valores[5] + '.pdf'

		# Retorna o PDF como resposta
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
			# força o download do arquivo 
			#response['Content-Disposition'] = f'attachment; filename="relatorio.pdf"'
			# exibe no navegador
            response['Content-Disposition'] = f'inline; filename="{nome_tabela}"'
        return response
    return None

