from datetime import datetime
from bs4 import BeautifulSoup
import pandas as pd
from src.configura_debug import *


def tabela_html_scraper(html, dt_inicial, dt_final):
    ''' faz um scrapping da página da tabela e retorna o dataframe da tabela'''
	
    soup = BeautifulSoup(html, 'html.parser')
    tabela = soup.find('table')

	# Extrai os cabecalhos
    #headers = [header.text.strip() for header in table.find_all('th')]
    cabecalhos = [cabecalho.text.strip() for cabecalho in tabela.find_all('th')]
    #info(f"headers:{headers}")

	# Extrai os dados das linhas da tabela
    
    linhas = []
    for linha in tabela.find_all('tr')[1:]:  # Ignora o cabeçalho
        cells = linha.find_all('td')
        linha_data = [cell.text.strip() for cell in cells]
        linhas.append(linha_data)

	# Converte '2023-01' em '01/2023', valores[2]-> data inicial e valores[3]-> data final
    datainicial = '/'.join(dt_inicial.split('-')[::-1])
    datafinal = '/'.join(dt_final.split('-')[::-1])

	# Converte as strings de data para objetos datetime para comparações
    data_inicial_dt = datetime.strptime(datainicial, '%m/%Y')
    data_final_dt = datetime.strptime(datafinal, '%m/%Y')

	# Filtra a lista para o período determinado
    resultado = [ registro for registro in linhas 
		   if data_inicial_dt <= datetime.strptime(registro[0], '%m/%Y') <= data_final_dt
		]

	# Exibe os dados extraídos
    '''info(f"Cabeçalhos: {cabecalhos}")
	for row in resultado:
		info(f"Linha:{row}")
		'''
    df = pd.DataFrame(resultado, columns=cabecalhos)
    #info(f"cabeçalhos:{cabecalhos}\nDataframe:\n{df}")

    return df, cabecalhos
