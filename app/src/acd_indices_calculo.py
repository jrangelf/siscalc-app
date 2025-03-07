from src.acd_api_indices import MatrizIndices
from src.acd_datetools import DateTools
from datetime import datetime
import pandas as pd

from src.configura_debug import * 

class Tabelas:
    def __init__(self,
                 tabela_juros: str,
                 tabela_pnep: str,
                 data_citacao: str,
                 data_atualizacao: str,
                 data_inicio_periodo: str,
                 data_final_periodo: str,
                 aplicar_selic: bool,
                 aplicar_selic_juros: bool):
        """
        Construtor da classe IamJuros.

        Args:
            tabela_juros: nome da tabela de juros.
            tabela_pnep: nome da tabela PNEP.
            data_citacao: data de citação.
            data_atualizacao: data de atualização.
            data_inicio_periodo: data de início do período de cálculo.
            data_final_periodo: data de fim do período de cálculo.
            aplicar_selic: indica se aplica SELIC.
            aplicar_selic_juros: indica se aplica SELIC nos juros.

        Raises:
            TypeError: Se algum dos parâmetros não for do tipo esperado.
        """
        
        # Validação de tipos
        if not all(isinstance(arg, str) for arg in [
            tabela_juros, tabela_pnep, data_citacao,
            data_atualizacao, data_inicio_periodo, data_final_periodo]):
            raise TypeError("Parâmetros de data e tabela devem ser strings")
            
        if not isinstance(aplicar_selic, bool) or not isinstance(aplicar_selic_juros, bool):
            raise TypeError("aplicar_selic e aplicar_selic_juros devem ser booleanos")

        self.tabela_juros = tabela_juros
        self.tabela_pnep = tabela_pnep
        self.data_citacao = data_citacao
        self.data_atualizacao = data_atualizacao
        self.data_inicio_periodo = data_inicio_periodo
        self.data_final_periodo = data_final_periodo
        self.aplicar_selic = aplicar_selic
        self.aplicar_selic_juros = aplicar_selic_juros

    def juros(self) -> pd.DataFrame:
        """
        Retorna o dataframe dos juros com base nos parâmetros da instância.
        """
        try:
            return self.obterTabelaJuros(
                self.tabela_juros,
                self.data_citacao,
                self.data_atualizacao,
                self.data_inicio_periodo,
                self.data_final_periodo,
                self.aplicar_selic,
                self.aplicar_selic_juros
            )
        except Exception as e:
            print(f"Erro em juros(): {e}")
            return pd.DataFrame()

    def indice(self) -> pd.DataFrame:
        """
        Retorna o dataframe do índice com base nos parâmetros da instância.
        """
        try:
            return self.obterTabelaIndice(
                self.tabela_pnep,
                self.data_inicio_periodo,
                self.data_final_periodo,
                self.data_atualizacao
            )
        except Exception as e:
            print(f"Erro em indice(): {e}")
            return pd.DataFrame()

    def selic(self) -> pd.DataFrame:
        """
        Retorna o dataframe da SELIC com base nos parâmetros da instância.
        """
        try:
            return self.obterTabelaSelic(
                self.data_citacao,
                self.data_atualizacao,
                self.data_inicio_periodo,
                self.data_final_periodo,
                self.aplicar_selic,
                self.aplicar_selic_juros
            )
        except Exception as e:
            print(f"Erro em selic(): {e}")
            return pd.DataFrame()
        
    def sufixo(self) -> pd.DataFrame:
        """
        Retorna o dataframe com juros, índice e SELIC combinados.
        """
        try:
            indice_df = self.indice()
            juros_df = self.juros()
            if self.aplicar_selic:
                selic_df = self.selic()
                parte = pd.merge(indice_df, juros_df, on='data', how='inner')
                sufixo = pd.merge(parte, selic_df, on='data', how='inner')
                info(f'# sufixo: \n{sufixo}')
            else:
                sufixo = pd.merge(indice_df, juros_df, on='data', how='inner')
            return sufixo
        except Exception as e:
            print(f"Erro ao combinar dataframes: {e}")
            return pd.DataFrame()    

    @classmethod
    def obterTabelaIndice(cls, 
                          tabela_pnep: str, 
                          data_inicio: str, 
                          data_final: str, 
                          data_atualizacao: str) -> pd.DataFrame:
        try:            
            tabela = MatrizIndices.matriz_tabela_pnep(tabela_pnep)
            tabela['data'] = DateTools.corrigir_data_series_coluna(tabela, 'data')            
            
            data_inicio = DateTools.converter_string_para_datetime_dia_primeiro(data_inicio)
            data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final)
            data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
            
            tabela_atualizada = cls.recalcular_indices(tabela, data_atualizacao)
            
            if not tabela_atualizada.empty:                        
                # o filtro deve conter o intervalo: data_inicio_calculo <-- --> data_final_calculo
                tabela_filtrada = tabela_atualizada[(tabela_atualizada['data'] >= data_inicio) & (tabela_atualizada['data'] <= data_final)]
                if not tabela_filtrada.empty:
                    # preencher com 1 da data_atualizacao até a data_final do cálculo
                    tabela_filtrada.loc[(tabela_filtrada['data'] >= data_atualizacao) & (tabela_filtrada['data'] <= data_final), 'indice_correcao'] = 1
                    recorte = tabela_filtrada[['data', 'indice_correcao']].copy()                    
                    return recorte
                else:                    
                    return tabela_atualizada            
                         
        except Exception as e:
            print(f"Erro em obterTabelaIndice: {e}")
            return 

    @classmethod
    def obterTabelaJuros(cls, 
                         nome_tabela: str, 
                         data_citacao: str, 
                         data_atualizacao: str, 
                         data_inicio: str, 
                         data_final: str, 
                         aplicar_selic: bool, 
                         aplicar_selic_juros: bool) -> pd.DataFrame:
        
        try:
            if aplicar_selic:                
                juros = MatrizIndices.matriz_tabela_juros(nome_tabela, data_citacao, data_atualizacao)               
                
                data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
                data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final)

                # zerar os juros da data_atualizacao até a data final do calculo
                juros.loc[(juros['data'] > data_atualizacao) & (juros['data'] <= data_final), 'taxa_juros_final_percentual'] = 0
                return juros
            else:
                juros = MatrizIndices.matriz_tabela_juros(nome_tabela, data_citacao, data_atualizacao)                
                data_inicio = DateTools.converter_string_para_datetime_dia_primeiro(data_inicio)
                data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final)
                #juros = juros[(juros['data'] >= data_inicio) & (juros['data'] <= data_final)]
                info(f'juros:\n{juros}')
                return juros
            
            
        except Exception as e:
            print(f"Erro em obterTabelaJuros: {e}")            
            return pd.DataFrame()

    @classmethod
    def obterTabelaSelic(cls, 
                         data_citacao: str, 
                         data_atualizacao: str, 
                         data_inicio: str, 
                         data_final: str, 
                         aplicar_selic: bool, 
                         aplicar_selic_juros: bool) -> pd.DataFrame:
        try:
            if aplicar_selic:
                selic = MatrizIndices.matriz_selic_acumulada(data_inicio, data_atualizacao)
                data_inicial = DateTools.converter_string_para_datetime_dia_primeiro(data_inicio)
                data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final) 
                # fazer um recorte data_inicio_calculo <-> data_final_periodo
                recorte = selic[(selic['data'] >= data_inicial) & (selic['data'] <= data_final)]                
                return recorte
            return []
                        
        except Exception as e:
            print(f"Erro em obterTabelaSelic: {e}")
            return

    @staticmethod
    def recalcular_indices(tabela: pd.DataFrame, 
                           data_atualizacao: datetime) -> pd.DataFrame:
        try:
            # [data  variacao_mensal  numero_indice  fator_vigente  indice_correcao]           
            data_ultima_linha = tabela['data'].iloc[-1]
            data_primeira_linha = tabela['data'].iloc[0]

            if data_atualizacao <= data_primeira_linha or data_atualizacao >= data_ultima_linha:
                return tabela

            novo_fator = tabela.loc[tabela['data'] == data_atualizacao, 'fator_vigente'].values
            novo_fator = novo_fator[0] if len(novo_fator) > 0 else None  # Evita erro de índice

            # percorre todo o dataframe calculando o novo indice que é o novo_fator/ fator_corrente
            if novo_fator:
                tabela['indice_correcao'] = novo_fator / tabela['fator_vigente']
                return tabela
            return
        
        except Exception as e:
            print(f"Erro em recalcular_indices: {e}")
            return 



















# from src.acd_api_indices import MatrizIndices
# from src.acd_datetools import *
# import pandas as pd

# class Tabelas:
#     """
#     Classe para calcular juros, IAM e SELIC com base em tabelas e datas.
#     """

#     def __init__(self,
#                  tabela_juros: str,
#                  tabela_pnep: str,
#                  data_citacao: str,
#                  data_atualizacao: str,
#                  data_inicio_periodo: str,
#                  data_final_periodo: str,
#                  aplicar_selic: bool,
#                  aplicar_selic_juros: bool):
#         """
#         Construtor da classe IamJuros.

#         Args:
#             tabela_juros: nome da tabela de juros.
#             tabela_pnep: nome da tabela PNEP.
#             data_citacao: data de citação.
#             data_atualizacao: data de atualização.
#             data_inicio_periodo: data de início do período de cálculo.
#             data_final_periodo: data de fim do período de cálculo.
#             aplicar_selic: indica se aplica SELIC.
#             aplicar_selic_juros: indica se aplica SELIC nos juros.

#         Raises:
#             TypeError: Se algum dos parâmetros não for do tipo esperado.
#         """
#         if not all(isinstance(arg, str) for arg in [tabela_juros, tabela_pnep, data_citacao, data_atualizacao, data_inicio_periodo, data_final_periodo]):
#             raise TypeError("Todos os parâmetros de data e tabela devem ser strings.")
#         if not isinstance(aplicar_selic, bool) or not isinstance(aplicar_selic_juros, bool):
#             raise TypeError("aplicar_selic e aplicar_selic_juros devem ser booleanos.")

#         self.tabela_juros = tabela_juros
#         self.tabela_pnep = tabela_pnep
#         self.data_citacao = data_citacao
#         self.data_atualizacao = data_atualizacao
#         self.data_inicio_periodo = data_inicio_periodo
#         self.data_final_periodo = data_final_periodo
#         self.aplicar_selic = aplicar_selic
#         self.aplicar_selic_juros = aplicar_selic_juros

#     def juros(self) -> pd.DataFrame:
#         """
#         Retorna o dataframe dos juros com base nos parâmetros da instância.
#         """
#         try:
#             return self.obterTabelaJuros(self.tabela_juros,
#                                          self.data_citacao,
#                                          self.data_atualizacao,
#                                          self.data_inicio_periodo,
#                                          self.data_final_periodo,
#                                          self.aplicar_selic,
#                                          self.aplicar_selic_juros)
#         except Exception as e:
#             print(f"Erro ao obter tabela de juros: {e}")
#             return pd.DataFrame()

#     def indice(self) -> pd.DataFrame:
#         """
#         Retorna o dataframe do índice com base nos parâmetros da instância.
#         """
#         try:
#             return self.obterTabelaIndice(self.tabela_pnep,
#                                           self.data_inicio_periodo,
#                                           self.data_final_periodo,
#                                           self.data_atualizacao)
#         except Exception as e:
#             print(f"Erro ao obter tabela de índice: {e}")
#             return pd.DataFrame()

#     def selic(self) -> pd.DataFrame:
#         """
#         Retorna o dataframe da SELIC com base nos parâmetros da instância.
#         """
#         try:
#             return self.obterTabelaSelic(self.data_citacao,
#                                          self.data_atualizacao,
#                                          self.data_inicio_periodo,
#                                          self.data_final_periodo,
#                                          self.aplicar_selic,
#                                          self.aplicar_selic_juros)
#         except Exception as e:
#             print(f"Erro ao obter tabela SELIC: {e}")
#             return pd.DataFrame()

#     def sufixo(self) -> pd.DataFrame:
#         """
#         Retorna o dataframe com juros, índice e SELIC combinados.
#         """
#         try:
#             indice_df = self.indice()
#             juros_df = self.juros()
#             selic_df = self.selic()

#             parte = pd.merge(indice_df, juros_df, on='data', how='inner')
#             sufixo = pd.merge(parte, selic_df, on='data', how='inner')

#             return sufixo
#         except Exception as e:
#             print(f"Erro ao combinar dataframes: {e}")
#             return pd.DataFrame()
        
# # self.tabela_juros = tabela_juros
# #         self.tabela_pnep = tabela_pnep
# #         self.data_citacao = data_citacao
# #         self.data_atualizacao = data_atualizacao
# #         self.data_inicio_periodo = data_inicio_periodo
# #         self.data_final_periodo = data_final_periodo
# #         self.aplicar_selic = aplicar_selic
# #         self.aplicar_selic_juros = aplicar_selic_juros

#     @classmethod
#     def obterTabelaIndice(self.tabela_pnep: str,
#                           self.data_inicio_periodo: str,
#                           self.data_final_periodo: str, 
#                           self.data_atualizacao: str # Optional[str] = None,  
#                             ) -> pd.DataFrame:
#         # tabela, data_inicial_calculo, data_final_calculo, data_atualizacao
#         tabela = MatrizIndices.matriz_tabela_pnep(nome_tabela)
#         tabela['data'] = DateTools.corrigir_data_series_coluna(tabela, 'data')
    
#         # converte as datas de string para timestamp
#         data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
#         data_inicial = DateTools.converter_string_para_datetime_dia_primeiro(data_inicial)
#         data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final)        
#         tabela_atualizada = cls.recalcular_indices(tabela, data_atualizacao)

#         if not tabela_atualizada.empty:                        
#             # o filtro deve conter o intervalo: data_inicio_calculo <-- --> data_final_calculo
#             tabela_filtrada = tabela_atualizada[(tabela_atualizada['data'] >= data_inicial) & (tabela_atualizada['data'] <= data_final)]
#             if not tabela_filtrada.empty:
#                # preencher com 1 da data_atualizacao até a data_final do cálculo
#                tabela_filtrada.loc[(tabela_filtrada['data'] >= data_atualizacao) & (tabela_filtrada['data'] <= data_final), 'indice_correcao'] = 1
#                recorte = tabela_filtrada[['data', 'indice_correcao']].copy()
#                return recorte
#             else:
#                return tabela_atualizada
    
        

#     @classmethod
#     def obterTabelaJuros(cls, 
#                         nome_tabela: str, 
#                         data_citacao: str, 
#                         data_atualizacao: str, 
#                         data_inicio_periodo: str, 
#                         data_final_periodo: str,
#                         aplicar_selic: bool,
#                         aplicar_selic_sobre_juros: bool
#                         ) -> pd.DataFrame:
       
#        if aplicar_selic:
#            juros = MatrizIndices.matriz_tabela_juros(nome_tabela, data_citacao, data_atualizacao) 
#            # zerar os juros da data_atualizacao até a data final do calculo
#            data_atualizacao = DateTools.converter_string_para_datetime_dia_primeiro(data_atualizacao)
#            data_final_periodo = DateTools.converter_string_para_datetime_dia_primeiro(data_final_periodo)
#            juros.loc[(juros['data'] > data_atualizacao) & (juros['data'] <= data_final_periodo), 'taxa_juros_final_percentual'] = 0
#            return juros
#        return


#     @classmethod
#     def obterTabelaSelic(cls, 
#                         data_citacao: str, 
#                         data_atualizacao: str, 
#                         data_inicio_calculo: str, 
#                         data_final_periodo: str,
#                         aplicar_selic: bool,
#                         aplicar_selic_sobre_juros: bool
#                         ) -> pd.DataFrame:
#        if aplicar_selic:
#            selic = MatrizIndices.matriz_selic_acumulada(data_inicio_calculo, data_atualizacao)
#            data_inicial = DateTools.converter_string_para_datetime_dia_primeiro(data_inicio_calculo)
#            data_final = DateTools.converter_string_para_datetime_dia_primeiro(data_final_periodo) 
#            # fazer um recorte data_inicio_calculo <-> data_final_periodo
#            recorte = selic[(selic['data'] >= data_inicial) & (selic['data'] <= data_final)]
#            return recorte
#        return
   
#     @staticmethod
#     def recalcular_indices(tabela: pd.DataFrame, 
#                           data_atualizacao: datetime) -> pd.DataFrame:

#        # [data  variacao_mensal  numero_indice  fator_vigente  indice_correcao]
#        #data_atualizacao = DateTools.ajusta_str_data_para_dia_primeiro(data_atualizacao)
#        #data_atualizacao = pd.to_datetime(data_atualizacao)
#        data_ultima_linha = tabela['data'].iloc[-1]
#        data_primeira_linha = tabela['data'].iloc[0]

#        if data_atualizacao <= data_primeira_linha or data_atualizacao >= data_ultima_linha:
#            return tabela

#        novo_fator = tabela.loc[tabela['data'] == data_atualizacao, 'fator_vigente'].values
#        novo_fator = novo_fator[0] if len(novo_fator) > 0 else None  # Evita erro de índice

#        # percorre todo o dataframe calculando o novo indice que é o novo_fator/ fator_corrente
#        if novo_fator:
#            tabela['indice_correcao'] = novo_fator / tabela['fator_vigente']
#            return tabela
#        return