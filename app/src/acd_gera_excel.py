from django.http import HttpResponse
from src.configura_debug import *

def gerarExcel(valores, headers, df):

    if valores[4] == "2":	
                
        # Salvar o DataFrame em um arquivo Excel temporário
        excel_file_path = "tabela.xlsx"
        df.to_excel(excel_file_path, index=False)        
        nome_tabela = valores[5] + '.xlsx'

        """ # Retornar o arquivo Excel como resposta - download direto
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(excel_file.read(), content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition'] = 'attachment; filename="tabela_selic.xlsx"'
            return response """

        # Retornar o arquivo Excel como resposta - mostra no browser / download
        with open(excel_file_path, 'rb') as excel_file:
            response = HttpResponse(
                excel_file.read(),
                content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
            )
            #response['Content-Disposition'] = 'inline; filename="tabela_selic.xlsx"'
            response['Content-Disposition'] = f'inline; filename="{nome_tabela}"'
            return response 
        
    return None


