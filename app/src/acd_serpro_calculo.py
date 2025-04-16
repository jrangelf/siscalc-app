import pandas as pd
from typing import Optional, Tuple, List, Dict

from src.acd_utils import *
from src.acd_api_serpro import *


class TabelasSerpro:


      @classmethod
      #async def tabelaTresDezessete (cls,
      def tabelaTresDezessete (cls, 
                               cpf: str, 
                               anoi: int, 
                               anof: int, 
                               basecalculo: list, 
                               basepgtos: list,
                               termo_inicial: str, # data inicial do cálculo
                               termo_final: str,   # data final do cálculo
                               data_citacao: str,
                               data_atualizacao: str,
                               percentual: int, 
                               orgao: Optional[int] = None,
                               pensionista: bool = False) -> Tuple [pd.DataFrame, pd.DataFrame, List]:      
         
         if pensionista:
            #df_base, df_pagtos, rubricas_cabecalho = await MatrizSerpro.matriz_tresdezessete_pensionista(cpf,
            df_base, df_pagtos, rubricas_cabecalho = MatrizSerpro.matriz_tresdezessete_pensionista(cpf,
                                                                                                   anoi,
                                                                                                   anof,
                                                                                                   basecalculo,
                                                                                                   basepgtos,
                                                                                                   termo_inicial,
                                                                                                   orgao)
         else:
             #df_base, df_pagtos, rubricas_cabecalho = await MatrizSerpro.matriz_tresdezessete(cpf,
             df_base, df_pagtos, rubricas_cabecalho = MatrizSerpro.matriz_tresdezessete(cpf,
                                                                                        anoi,
                                                                                        anof,
                                                                                        basecalculo,
                                                                                        basepgtos,
                                                                                        termo_inicial,
                                                                                        orgao)
         
         data_inicio_calculo = DateTools.converter_string_para_datetime_dia_primeiro(termo_inicial)
         data_final_calculo = DateTools.converter_string_para_datetime_dia_primeiro(termo_final)
      
         # separa o dataframe do período de cálculo
         df_calculo = df_base[(df_base['datapagto'] >= data_inicio_calculo) & (df_base['datapagto'] <= data_final_calculo)]
      
         # if df_pagtos:
         #     df_pagamentos = df_pagtos[(df_pagtos.iloc[:, 1:] != 0).any(axis=1)]
         #     info(f"\n\nacd_serpro_calculo\n[     DF_PAGTOS    ]\n\n\n{df_pagtos}")
         # else:
         #     df_pagamentos = None

         if isinstance(df_pagtos, pd.DataFrame) and not df_pagtos.empty:
            # Remove linhas onde todas as colunas (exceto a primeira) são zero
            df_pagamentos = df_pagtos[(df_pagtos.iloc[:, 1:] != 0).any(axis=1)]
            
            # Log das informações do DataFrame original para depuração
            #info(f"\n\nacd_serpro_calculo\n[     DF_PAGTOS    ]\n\n\n{df_pagtos}")
         else:
            df_pagamentos = None

         
         #check if any value in the specified columns is non-zero. This approach is conceptually equivalent but avoids using the ~ operator.
         #df_pagamentos = df_pagtos[(df_pagtos.iloc[:, 1:] != 0).any(axis=1)] # mais conciso e eficiente

         # it sums the values in the specified columns and filter rows where the sum is greater than zero. This works because the sum of zeros is zero
         #df_pagamentos = df_pagtos[df_pagtos.iloc[:, 1:].sum(axis=1) > 0]


         return df_calculo, df_pagamentos, rubricas_cabecalho














      @classmethod
      
      def tabela_2886_sicape(cls, 
                             simplificado,
                             completo,
                             resultado):
         """
         este método é responsável por criar os dataframes C, F e R de cada exequente.
         deve-se processar:
            limitação do óbito, 
            o cálculo do teto constitucional, 
            pró-rata, 
            percentual e percentual residual,
            caso o orgao seja ministerio saude, utilizar os 33%
            pagamentos administrativos também aqui.
         os dataframes estão prontos para receberem o sufixo

         este método chama o método da matriz_2886 para criar os raw_dataframes e os devolve para que sejam processados por este método.          
         """         
         
         # cria um dicionário para os campos e uma lista de dicionários para as rubricas retirando as de tipo 'N'
         campos, rubricas_base_2886 = Utils.extrair_campos(resultado)

         # filtrar apenas as rubricas de rendimentos da extração do sicape
         linhas_rendimento_arquivo_completo = Utils.filtrar_rendimentos_sicape(completo)         
         
         # obter os códigos das rubricas da extração de rendimentos filtrada
         lista_rubricas_extracao = Utils.obter_rubricas_extracao_sicape(linhas_rendimento_arquivo_completo)

         # obter uma lista das rubricas de extração que estão contidas nas rubricas da base 2886
         lista_rubricas_calculo = Utils.extrair_fitas_sicape(rubricas_base_2886, lista_rubricas_extracao)
         
         # criar uma lista de dicionários separando os exequentes com suas respectivas rubricas extraídas
         ficha = Utils.processar_arquivo_completo_e_simplificado_sicape(simplificado, 
                                                                           linhas_rendimento_arquivo_completo, 
                                                                           lista_rubricas_calculo)
         
         # obter a descricao das rubricas do calculo
         descricao_rubricas_calculo = Utils.obter_descricao_rubricas_sicape(ficha)         

         dicionario_dataframes = MatrizSerpro.matriz_2886_sicap(ficha, descricao_rubricas_calculo, lista_rubricas_calculo, campos)

         return dicionario_dataframes
         

   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
   
      @classmethod
      def tabelaTrezDezessete (cls, 
                            cpf: str, 
                            anoi: int, 
                            anof: int, 
                            basecalculo: list, 
                            basepgtos: list,
                            termo_inicial: str, # data inicial do cálculo
                            termo_final: str,   # data final do cálculo
                            data_citacao: str,
                            data_atualizacao: str,
                            percentual: int, 
                            orgao: Optional[int] = None) -> Tuple [pd.DataFrame, pd.DataFrame, List]:      
      
         df_base, df_pagtos, rubricas_cabecalho = MatrizSerpro.matriz_trezdezessete(cpf,
                                                                                  anoi,
                                                                                  anof,
                                                                                  basecalculo,
                                                                                  basepgtos,
                                                                                  termo_inicial,
                                                                                  orgao)
      
         data_inicio_calculo = DateTools.converter_string_para_datetime_dia_primeiro(termo_inicial)
         data_final_calculo = DateTools.converter_string_para_datetime_dia_primeiro(termo_final)
      
         # separa o dataframe do período de cálculo
         df_calculo = df_base[(df_base['datapagto'] >= data_inicio_calculo) & (df_base['datapagto'] <= data_final_calculo)]
      
         # Eliminando as linhas onde todos os valores são zero (exceto a primeira coluna da data)
         #df_pagamentos = df_pagtos[~(df_pagtos.iloc[:, 1:] == 0).all(axis=1)]

         df_pagamentos = df_pagtos[(df_pagtos.iloc[:, 1:] != 0).any(axis=1)]
      
         #check if any value in the specified columns is non-zero. This approach is conceptually equivalent but avoids using the ~ operator.
         #df_pagamentos = df_pagtos[(df_pagtos.iloc[:, 1:] != 0).any(axis=1)] # mais conciso e eficiente

         # it sums the values in the specified columns and filter rows where the sum is greater than zero. This works because the sum of zeros is zero
         #df_pagamentos = df_pagtos[df_pagtos.iloc[:, 1:].sum(axis=1) > 0]


         return df_calculo, df_pagamentos, rubricas_cabecalho
   



   
