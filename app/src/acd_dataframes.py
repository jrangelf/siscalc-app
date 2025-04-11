import csv

from typing import List, Optional, Tuple, Dict

from src.acd_api_serpro import MatrizSerpro
from src.acd_api_indices import MatrizIndices
from src.acd_indices_calculo import Tabelas
from src.acd_serpro_calculo import TabelasSerpro

from src.configura_debug import *
from src.acd_datetools import *
from src.api_indice import *
from src.acd_utils import *

import pandas as pd

class DataframeAjustes:
    
    @classmethod
    def ajustar_df_basepagtos(cls, basepagtos, sufixo, aplicarSELIC, selicJuros, percentual):
        
        if not basepagtos.empty and not sufixo.empty:
            basepagtos['soma'] = basepagtos.iloc[:, 1:].sum(axis=1)            
            colunas_basepagtos = basepagtos.columns.tolist()            
            basepagtos_sufixo = pd.merge(
                basepagtos,
                sufixo,
                left_on='datapagto',    # coluna de data em basepagtos
                right_on='data',        # coluna de data em sufixo
                how='inner'             # usar apenas as datas que existam em ambos os dataframes
            )

            # remover a coluna duplicada 'data', já possui datapagto
            basepagtos_sufixo.drop(columns=['data'], inplace=True)            

            # incluir as colunas adicionais após a inclusão do sufixo
            valor_percentual = int(percentual)/100
            basepagtos_sufixo['percentual'] = valor_percentual
            basepagtos_sufixo['valor_devido'] = basepagtos_sufixo['soma'] * basepagtos_sufixo['percentual']
            basepagtos_sufixo['principal_atualizado'] = basepagtos_sufixo['valor_devido'] * basepagtos_sufixo['indice_correcao']
            basepagtos_sufixo['valor_juros'] = basepagtos_sufixo['principal_atualizado'] * (basepagtos_sufixo['taxa_juros_final_percentual'] / 100)
            
            if aplicarSELIC:
                basepagtos_sufixo['TOTAL EM DEZ/2021'] = basepagtos_sufixo['principal_atualizado'] + basepagtos_sufixo['valor_juros']
                basepagtos_sufixo['valor_selic'] = basepagtos_sufixo['TOTAL EM DEZ/2021'] * basepagtos_sufixo['selic_acumulada']
                basepagtos_sufixo['TOTAL BRUTO'] = basepagtos_sufixo['TOTAL EM DEZ/2021'] + basepagtos_sufixo['valor_selic']
                # Reordenar as colunas na ordem desejada            
                colunas_ordenadas = colunas_basepagtos + [
                    'percentual', 'valor_devido', 'indice_correcao', 
                    'principal_atualizado', 'taxa_juros_final_percentual', 'valor_juros', 
                    'TOTAL EM DEZ/2021', 'selic_acumulada', 'valor_selic', 'TOTAL BRUTO' 
                ]
            else:
                basepagtos_sufixo['TOTAL BRUTO'] = basepagtos_sufixo['principal_atualizado'] + basepagtos_sufixo['valor_juros']
                # Reordenar as colunas na ordem desejada            
                colunas_ordenadas = colunas_basepagtos + [
                'percentual', 'valor_devido', 'indice_correcao', 
                'principal_atualizado', 'taxa_juros_final_percentual', 'valor_juros', 'TOTAL BRUTO'
                ]

            basepagtos_sufixo = basepagtos_sufixo[colunas_ordenadas]
            info(f"colunas ordenadas\n{colunas_ordenadas}")
            info(f"\n\nacd_dataframes\n[ PAGAMENTOS ADMINISTRATIVOS ]\n\n{basepagtos_sufixo}")

            if not basepagtos_sufixo.empty:
                   return basepagtos_sufixo            
            return
        

    @classmethod
    def ajustar_df_basecalculo(cls, basecalculo, sufixo, aplicarSELIC, selicJuros):

        if not basecalculo.empty and not sufixo.empty:
            colunas_basecalculo = basecalculo.columns.tolist()
            # incluir o sufixo do dataframe de basecalculos
            basecalculo_sufixo = pd.merge(
                basecalculo,
                sufixo,
                left_on='datapagto',    # coluna de data em basecalculo
                right_on='data',        # coluna de data em sufixo
                how='inner'             # usar apenas as datas que existam em ambos os dataframes
            )            
            basecalculo_sufixo.drop(columns=['data'], inplace=True)
            basecalculo_sufixo['valor_devido'] = basecalculo_sufixo['soma'] * basecalculo_sufixo['(%)']
            basecalculo_sufixo['principal_atualizado'] = basecalculo_sufixo['valor_devido'] * basecalculo_sufixo['indice_correcao']
            basecalculo_sufixo['valor_juros'] = basecalculo_sufixo['principal_atualizado'] * (basecalculo_sufixo['taxa_juros_final_percentual'] / 100)
            
            if aplicarSELIC:
                basecalculo_sufixo['TOTAL EM DEZ/2021'] = basecalculo_sufixo['principal_atualizado'] + basecalculo_sufixo['valor_juros']
                basecalculo_sufixo['valor_selic'] = basecalculo_sufixo['TOTAL EM DEZ/2021'] * basecalculo_sufixo['selic_acumulada']
                basecalculo_sufixo['TOTAL BRUTO'] = basecalculo_sufixo['TOTAL EM DEZ/2021'] + basecalculo_sufixo['valor_selic']
                # Reordenar as colunas na ordem desejada            
                colunas_ordenadas = colunas_basecalculo + [
                    'indice_correcao', 'principal_atualizado', 'taxa_juros_final_percentual', 'valor_juros', 
                    'TOTAL EM DEZ/2021', 'selic_acumulada', 'valor_selic', 'TOTAL BRUTO' 
                ]
            else:
                basecalculo_sufixo['TOTAL BRUTO'] = basecalculo_sufixo['principal_atualizado'] + basecalculo_sufixo['valor_juros']
                # Reordenar as colunas na ordem desejada            
                colunas_ordenadas = colunas_basecalculo + [
                'indice_correcao','principal_atualizado', 'taxa_juros_final_percentual', 'valor_juros', 'TOTAL BRUTO'
                ]

            basecalculo_sufixo = basecalculo_sufixo[colunas_ordenadas]
            info(f"colunas ordenadas:\n{colunas_ordenadas}")
            info(f"\n\nacd_dataframes\n[ CÁLCULO 3,17% ]\n\n{basecalculo_sufixo}")

            if not basecalculo_sufixo.empty:
                   return basecalculo_sufixo            
            return