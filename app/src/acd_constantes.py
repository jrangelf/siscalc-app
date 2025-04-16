from decouple import config, Csv


API_INDICE = config('API_INDICE')
API_SERPRO = config('API_SERPRO')

TABELASELIC = config('TABELASELIC')
DATASELIC = config('DATASELIC')

SQLALCHEMY_DATABASE_URL = config('SQLALCHEMY_DB_URL')

TOKEN = config('TOKEN')
WSDL = config('WSDL')

NOREGS='Não há registro'

MODELO = {
          'datapagto': 'MESANO', 
          'soma': 'SOMA', 
          'valor_devido': 'VALOR DEVIDO',
          'percentual': 'PAGTOS ADM (%)', 
          'indice_correcao': 'IAM', 
          'principal_atualizado': 'PRINCIPAL ATUALIZADO', 
          'taxa_juros_final_percentual': 'JUROS (%)', 
          'valor_juros': 'VALOR JUROS', 
          'selic_acumulada': 'TAXA SELIC A PARTIR DE DEZ/2021 (EC 113/2021)', 
          'valor_selic': 'VALOR SELIC'
        }

