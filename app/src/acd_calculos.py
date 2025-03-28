from src.acd_api_serpro import MatrizSerpro
from src.acd_serpro_calculo import TabelasSerpro

from src.configura_debug import *

import pandas as pd


class Calculos:

    @classmethod
    def calcular_2886_sicape(cls,
                             simplificado,
                             completo,
                             resultado):
        
        
        
        # montar um dicionário de dataframes para cada cpf de exequente
        prefixo_2886_df = TabelasSerpro.tabela_2886_sicape(simplificado, completo, resultado)
        
        # buscar Iam, juros, selic
        # aplicar teto
        # aplicar percentuais
        # aplicar pro-rata
        # aplicar segundo percentual.

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option("display.float_format", "{:.2f}".format)



        # # Exibir o resultado
        # for exequente in prefixo_2886_df:
        #     info(f"Exequente: {exequente['nome']} (CPF: {exequente['cpf']})")
        #     info("DataFrames:")
        #     for idx, categoria in enumerate(['C', 'F', 'R', 'P']):
        #         info(f"DataFrame {categoria}:")
        #         info(f"\n{exequente['dataframes'][idx]}\n")
        #     info("\n")

    

        return prefixo_2886_df


    
    
    
    
    
    
    
    
    
    
    def calcular_317_sicape(cls,a,b):
        ...