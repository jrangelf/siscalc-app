from datetime import datetime, timedelta

from src.configura_debug import *

from src.api_indice import ApiIndice
from src.acd_datetools import DateTools
from src.acd_constantes import TABELASELIC, DATASELIC

import pandas as pd

from typing import Optional

"""Este módulo intermedeia a comunicação entre o siscalc e a busca de dados na api indices """


class MatrizIndices:

   @classmethod   
   def matriz_selic_acumulada(cls,
                              data_inicio_calculo: str,
                              data_atualizacao: str
                             ) -> pd.DataFrame:
        
        tabela_selic = cls.carregar_tabela_selic(TABELASELIC)
        tabela_selic['data'] = DateTools.corrigir_data_series(tabela_selic['data'])
        data_inicio_selic = DateTools.converter_string_para_datetime(DATASELIC) # EC 113
                
        if not tabela_selic.empty:
            data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
            data_inicio_calculo = DateTools.converter_string_para_datetime_dia_primeiro(data_inicio_calculo)
            selic_acumulada = tabela_selic.loc[tabela_selic['data'] == data_atualizacao, 'selic_acumulada'].values
            selic_acumulada = selic_acumulada[0] if len(selic_acumulada) > 0 else None  

            datas = pd.date_range(start=data_inicio_calculo, 
                                  end=data_inicio_selic, 
                                  freq='MS'
                                 )
                        
            matriz_p1 = pd.DataFrame({ 'data': datas, 'selic_acumulada': selic_acumulada})
            matriz_p1['selic_acumulada'] = selic_acumulada            
            matriz_p2 = tabela_selic.loc[(tabela_selic['data'] <= data_atualizacao) &
                                              (tabela_selic['data'] > data_inicio_selic),
                                       ['data', 'selic_acumulada']
                                      ].copy()

            # Filtra as linhas no intervalo de datas e aplica a operação
            condicao = (matriz_p2['data'] > data_inicio_selic) & (matriz_p2['data'] <= data_atualizacao)
            matriz_p2.loc[condicao, 'selic_acumulada'] = selic_acumulada - matriz_p2.loc[condicao, 'selic_acumulada']
            matriz = pd.concat([matriz_p1, matriz_p2], ignore_index=True)        
        return matriz
   
    
   @classmethod
   def matriz_tabela_juros(cls, 
                           nome_tabela:str,
                           data_citacao: str, 
                           data_atualizacao: str ) -> pd.DataFrame:
        
        data_citacao = DateTools.converter_string_para_datetime_dia_primeiro(data_citacao)
        data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
        
        dados_brutos = cls.carregar_tabela_juros(nome_tabela)
        df = pd.DataFrame(dados_brutos)        

        #df['data'] = pd.to_datetime(df['data'])
        #df['data'] = DateTools.corrigir_data_series(df['data'])
        df['data'] = DateTools.corrigir_data_series_coluna(df, 'data')

        data_primeira_linha = df['data'].iloc[0]
        data_ultima_linha = df['data'].iloc[-1]

        if data_citacao < data_primeira_linha:
            data_da_citacao = data_primeira_linha
        else:
            data_da_citacao = data_citacao

        if data_atualizacao > data_ultima_linha:
            data_da_atualizacao = data_ultima_linha
        else:
            data_da_atualizacao = data_atualizacao

        df['juros_acumulados_2'] = df['juros_acumulados'].where(df['data'] > data_da_citacao,0)
        termo1 = df.loc[df['data'] == data_da_atualizacao, 'juros_acumulados'].values[0]
        termo2 = df.loc[df['data'] == data_da_citacao, 'juros_acumulados'].values[0]
        valor = termo1 - termo2
        df['taxa_juros_final'] = 0
        df['taxa_juros_final'] = df['taxa_juros_final'].astype(float) 

        # Preenche a coluna 'taxa_juros_final' iterativamente
        for i, row in df.iterrows():
            if row['juros_acumulados_2'] == 0:
                df.at[i, 'taxa_juros_final'] = valor
            else:
                if i == 0:  # Primeira linha
                    df.at[i, 'taxa_juros_final'] = row['juros']
                else:
                    juros_final_anterior = df.at[i - 1, 'taxa_juros_final']
                    df.at[i, 'taxa_juros_final'] = juros_final_anterior - row['juros']

        df['taxa_juros_final_percentual'] = df['taxa_juros_final'] * 100
        colunas_para_arredondar = ['juros','juros_acumulados', 'juros_acumulados_2', 'taxa_juros_final', 'taxa_juros_final_percentual']
        df[colunas_para_arredondar] = df[colunas_para_arredondar].round(8)
                
        seleciona_colunas = df[['data', 'taxa_juros_final_percentual']].copy()        
        return seleciona_colunas

   @classmethod
   def matriz_tabela_pnep(cls, nome_tabela:str) -> pd.DataFrame:
        dados_brutos = cls.carregar_tabela_pnep(nome_tabela)
        df = pd.DataFrame(dados_brutos)
        df['data'] = pd.to_datetime(df['data'])
        colunas_para_arredondar = ['variacao_mensal','numero_indice','fator_vigente','indice_correcao']
        df[colunas_para_arredondar] = df[colunas_para_arredondar].round(10)
        return df
   
   @classmethod
   def carregar_tabela_pnep (cls, nome_tabela: str) -> list:
        dados_brutos = ApiIndice.get_tabela(nome_tabela) 
        dados = []
        dict_linha = {}
        for linha in dados_brutos:
            dict_linha = {
                'data': linha['data'], 
                'variacao_mensal': linha['variacao_mensal'],
                'numero_indice': linha['numero_indice'],
                'fator_vigente': linha['fator_vigente'],
                'indice_correcao': linha['indice_correcao']
            }            
            dados.append(dict_linha)
        return dados

   @classmethod
   def carregar_tabela_juros (cls, nome_tabela: str) -> list:
        dados_brutos = ApiIndice.get_tabela(nome_tabela) 
        dados = []
        dict_linha = {}
        for linha in dados_brutos:
            dict_linha = {
                'data': linha['data'],
                'juros': linha['juros_mensal'],
                'juros_acumulados': linha['juros_acumulados']
            }            
            dados.append(dict_linha)
        return dados        
    
   @classmethod
   def carregar_tabela_selic(cls, nome_tabela: str) -> pd.DataFrame:
        dados_brutos = ApiIndice.get_tabela(nome_tabela) 
        dados = []
        dict_linha = {}
        for linha in dados_brutos:
             dict_linha = {
                 'data': linha['data'],
                 'selic': linha['selic'],
                 'selic_acumulada': linha['selic_acumulada'],
                 'selic_acumulada_mensal': linha['selic_acumulada_mensal'],                 
             }            
             dados.append(dict_linha)

        df = pd.DataFrame(dados)
        colunas_para_arredondar = ['selic','selic_acumulada', 'selic_acumulada_mensal']
        df[colunas_para_arredondar] = df[colunas_para_arredondar].round(8)
        df['data'] = pd.to_datetime(df['data'])        
        return df
    
    
    



        




        