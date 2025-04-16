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
from src.acd_constantes import MODELO

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

            #info(f"\n\nacd_calculos\n[ PAGAMENTOS ADMINISTRATIVOS ]\n\n{basepagtos_sufixo}")
        

            if not basepagtos_sufixo.empty:
                   basepagtos_sufixo_renomeado = cls.renomear_colunas_dataframe(basepagtos_sufixo, MODELO)
                   #info(f"colunas_basepagtos:{basepagtos_sufixo_renomeado.columns}")
                   return basepagtos_sufixo_renomeado            
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
            
            #info(f"\n\nacd_dataframes\n[ CÁLCULO 3,17% ]\n\n{basecalculo_sufixo}")            

            if not basecalculo_sufixo.empty:
                   basecalculo_sufixo_renomeado = cls.renomear_colunas_dataframe(basecalculo_sufixo, MODELO)                   
                   #info(f"\n\ncolunas_basecalculo:{basecalculo_sufixo_renomeado.columns}\n")
                   return basecalculo_sufixo_renomeado            
            return
        
   
    
    @classmethod
    def renomear_colunas_dataframe(cls, dtframe, modelo, lista_adicional=None):
        """ renomeia as colunas de um dataframe baseado no modelo passado como referência. 
            Pode-se acrescentar novos valores ao dicionario modelo por meio da lista_adicional
            modelo = {
                 'datapagto': 'MÊS/ANO', 
                 'soma': 'SOMA', 
                 'valor_devido': 'VALOR DEVIDO', 
                 'indice_correcao': 'IAM', 
                 'principal_atualizado': 'PRINCIPAL ATUALIZADO', 
                 'taxa_juros_final_percentual': 'JUROS (%)', 
                 'valor_juros': 'VALOR JUROS', 
                 'selic_acumulada': 'TAXA SELIC A PARTIR DE DEZ/2021 (EC 113/2021)', 
                 'valor_selic': 'VALOR SELIC'
                 }
            lista_adicional = [
                    {1: 'VENCIMENTO BÁSICO'}, 
                    {13: 'ANUENIO - ART.244, LEI 8112/90'}, 
                    {79: 'IND TRANSPORTE DEC 3184/99'}, 
                    {192: 'GRAT.EST.FISC.ARREC.TRIB.FED/A'}, 
                    {220: 'FERIAS - ADICIONAL 1/3'}, 
                    {10288: 'DECISAO JUDICIAL N TRAN JUG AT'}, 
                    {82174: 'VANTAGEM ADMINIST. 3,17% - AT'}, 
                    {82229: 'VANT.PEC.INDIVIDUAL-L.10698/03'}            
            ]
        """
        mapeamento = modelo.copy() # dicionário que apresenta o mapeamento dos nomes dos campos a serem substituidos
        #info(f"mapeamento:\n{mapeamento}")
        
        # Adicionar lista_cabecalho ao mapeamento já fornecido
        if lista_adicional:
            for dicionario in lista_adicional:
                for chave, valor in dicionario.items():
                    mapeamento[chave] = valor

        novas_colunas = []
        for coluna in dtframe.columns:
            if coluna in mapeamento:  # Se a coluna estiver no mapeamento, substituir pelo nome descritivo
                novas_colunas.append(mapeamento[coluna])
            else:  # Caso contrário, manter o nome original
                novas_colunas.append(coluna)
        dtframe.columns = novas_colunas       
        
        return dtframe


    @classmethod
    def adicionar_nova_linha_cabecalho(cls, dtframe, lista, novalinha):
        """ adiciona nova linha ao dataframe.
            lista é o cabeçalho atual e será a segunda linha do dataframe.            
            nova_linha é um dicionário utilizado para inserir na primeira linha do dataframe, acima da coluna indicada por cada chave.
            Exemplo:
            lista = ['datapagto', 'soma', 'valor_devido', 1, 13, 220] 
            novalinha = {1: 'VENCIMENTO', 220: 'FERIAS', 13: 'ATS' }
            resultado:
            	            		                 1	     13	  220
            datapagto	SOMA	valor_devido	VENCIMENTO	ATS	FERIAS
        """

        linha_superior = [col if col in novalinha else '' for col in lista]
        linha_inferior = [novalinha.get(col, col) for col in lista]
        novo_cabecalho = pd.MultiIndex.from_arrays([linha_superior, linha_inferior])
        dtframe.columns = novo_cabecalho
        # info(f'Dataframe: \n\n{dtframe}\n\n')
        return dtframe      
        
            


