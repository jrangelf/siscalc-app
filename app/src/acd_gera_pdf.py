from django.http import HttpResponse
from fpdf import FPDF
import pandas as pd

def gerarPDF(valores, headers, df):
    if valores[4] == "1":
        pdf_path = "relatorio.pdf"

        # Criar o objeto PDF
        pdf = FPDF()

        # Configuração básica da página
        if len(headers) <= 4:
            pdf.add_page()  # Tamanho A4 padrão
        else:
            pdf.add_page(orientation='L')  # Página no formato paisagem

        # Configurações da fonte
        pdf.set_font('helvetica', 'B', 10)
        
        # Adicionando o cabeçalho da tabela
        for i, header in enumerate(headers):
            pdf.cell(40, 10, header, border=1, align='C')
        pdf.cell(0, 10, '', ln=True)  # Quebra de linha após o cabeçalho
        
        # Adicionando os dados da tabela
        pdf.set_font('helvetica', '', 10)
        for row in df.values.tolist():
            for cell in row:
                pdf.cell(40, 10, str(cell), border=1, align='C')
            pdf.cell(0, 10, '', ln=True)  # Quebra de linha após cada linha de dados

        # Salva o PDF
        pdf.output(pdf_path)

        # Retorna o PDF como resposta
        with open(pdf_path, 'rb') as pdf_file:
            response = HttpResponse(pdf_file.read(), content_type='application/pdf')
            # Exibe no navegador
            response['Content-Disposition'] = f'inline; filename="relatorio.pdf"'
        return response

    return None