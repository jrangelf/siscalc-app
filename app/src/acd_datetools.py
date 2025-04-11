from datetime import datetime, timedelta
import pandas as pd

from src.configura_debug import *


class DateTools:
    
    @staticmethod
    def corrigir_data_series(data_series: pd.Series) -> pd.Series:
        """
        Corrige a data trocando o mês e o dia em cada valor da Série.
        Para cada valor datetime na série, o mês é substituído pelo dia
        e o dia é substituído pelo mês.
        """
        # Usando .dt para acessar diretamente os componentes de data e aplicar a troca
        return data_series.apply(
            lambda x: x.replace(day=x.month, month=x.day) if pd.notna(x) else x
        )

    @staticmethod
    def corrigir_data_series_coluna(df, coluna: str):
        # Se a coluna não estiver no formato datetime64, converte para datetime
        # df['data'] = corrigir_data_series_coluna(df, 'data')
        if not pd.api.types.is_datetime64_any_dtype(df[coluna]):
            df[coluna] = pd.to_datetime(df[coluna])
        # Troca o mês e o dia se a data for válida
        df[coluna] = df[coluna].apply(lambda x: x.replace(day=x.month, month=x.day) if pd.notna(x) else x) #verifica se um valor não é NaN (Not a Number, ou seja, um valor ausente ou nulo)
        return df[coluna]

    
    @staticmethod
    def converter_data_serie_ano_mes_datetime(df: pd.Series, coluna: str):
        return pd.to_datetime(df[coluna], format='%Y%m')
    
    
    @staticmethod
    def calcular_pro_rata(data: str) -> float:  
        """Calcula o pro-rata e ajusta a data de início"""
        dia = data[:2]        
        pro_rata = 0
        if dia != "01":
            pro_rata = ((30 - int(dia)) + 1) / 30            
        else:
            pro_rata = 1
        return pro_rata
    
    @staticmethod
    def converter_ano_mes_dia_para_string(data: str) -> str:
        """ Converte a string 2025-07-01 na string 01/07/2025 """
        partes = data.split("-")
        data_formatada = str(f"{partes[2]}/{partes[1]}/{partes[0]}")
        #info(f'data: {data_formatada}')
        return data_formatada #f"{partes[2]}/{partes[1]}/{partes[0]}"

    
    
    
    
    # # Exemplo de uso
    # data = {'data': ['30/07/2024', '15/08/2023', '12/11/2022']}
    # df = pd.DataFrame(data)
    # # Aplicando a correção
    # df['data'] = corrigir_data_series(df, 'data')
    # print(df)

    
    # @staticmethod
    # def corrigir_data_series(data_series: datetime) -> datetime:
    #     # Trocar o mês e o dia usando pandas .dt
    #     return data_series.apply(lambda x: x.replace(day=x.month, month=x.day) if pd.notnull(x) else x)

    
    @staticmethod
    def dia_de_hoje() -> datetime:
        '''Retorna a data e hora atual.'''
        return datetime.now()
    
    @staticmethod
    def converter_string_para_datetime(data_str: str) -> pd.Timestamp:
        """
        Converte uma string no formato 'dd/mm/yyyy' para um objeto datetime (pd.Timestamp).
        Exemplo: '01/07/2023' será convertido para '2023-07-01 00:00:00+0000'.
        """
        data_obj = datetime.strptime(data_str, "%d/%m/%Y")
        return data_obj
    
    @staticmethod
    def converter_string_para_datetime_dia_primeiro(data: str) -> pd.Timestamp:
        """
        Converte uma string de data no formato 'dd/mm/yyyy' para um objeto datetime,
        ajustando para o primeiro dia do mês e definindo a hora como 00:00:00.
        """
        data_obj = datetime.strptime(data, '%d/%m/%Y')
        primeiro_dia_mes = data_obj.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        return primeiro_dia_mes
    
    @staticmethod
    def converter_string_ano_mes_para_datetime(data: str) -> pd.Timestamp:
        """ converte uma string de data no formato 'YYYYMM' para um objeto datetime """        
        data_obj = datetime.strptime(data, '%Y%m')
        data_convertida = data_obj.strftime("%Y-%m-%d")
        return data_convertida

    @staticmethod
    def formatar_datetime_ano_mes_dia_para_str(data: datetime) -> str:
        """ Formata um objeto datetime em uma string no formato ('%Y-%m-%d')"""
        return data.strftime("%Y-%m-%d")
    
    @staticmethod
    def formatar_str_dmy_para_ymd(data: str) ->str:
        ''' converte a string 01/07/2023 em 2023-07-01 '''
        partes = data.split("/")
        nova_data = f"{partes[2]}-{partes[1]}-{partes[0]}"
        return nova_data



    @staticmethod
    def formatar_data_str_dmy(self, data):
        
        return data.strftime("%d/%m/%Y")
    
    @staticmethod
    def incrementa_mes_str(self, data_str):
        # Converter a string de data para um objeto datetime
        data = datetime.strptime(data_str, '%d/%m/%Y')
        # Incrementar o mês
        data_proximo_mes = data.replace(day=1) + timedelta(days=32)
        data_proximo_mes_formatado = data_proximo_mes.strftime('01/%m/%Y')
        return data_proximo_mes_formatado
    
    @staticmethod
    def ajusta_str_data_para_dia_primeiro(str_data) -> str :
        """ Formata uma string de data no formato 'DD/MM/AAAA' ou 'MM/AAAA' para '01/MM/AAAA'. """
        partes = str_data.strip().split('/')
        if len(partes) == 3:    # Caso com dia, mês e ano (ignora o dia)
            _, mes, ano = partes
        elif len(partes) == 2:  # Caso apenas com mês e ano
            mes, ano = partes
        else:
            raise ValueError("Formato de data inválido. Use 'DD/MM/AAAA' ou 'MM/AAAA'.")
        mes = mes.zfill(2)  # Garante que o mês tenha dois dígitos
        return f"01/{mes}/{ano}"
    
    

    @staticmethod
    def verificar_data_atualizacao(self, codigo, data_atual, data_log):
        ''' 1. atualiza o campo processar para 1 caso a diferença de meses entre a data atual e a 
            data da ultima atualizacao de cada tabela de indexadores for maior ou igual a 2
            2. atualiza o campo processar para 1 caso a diferenca de meses entre a data atual e a 
            data da ultima atualizacao de cada tabela de indices pnep for maior ou igual a 1        
        '''
        # print(f"\n====================================")
        # print(f"codigo:{codigo}\ndata_atual:{data_atual}\ndata_log:{data_log}")
        # print(f"\n====================================")

        diferenca_meses = (data_atual.year - data_log.year) * 12 + (data_atual.month - data_log.month)        

        if diferenca_meses >= 2 and codigo < 200:
            return True
        elif diferenca_meses >= 1 and 200 <= codigo < 300:
            return True
        elif diferenca_meses >= 1 and 300 <= codigo < 400:
            return True
        return False    
    
    def incrementa_mes_obj(self, data):
        ''' converte 2023-07-01 00:00:00+0000 em 2023-08-01 00:00:00+0000'''    
        if data is not None:        
            ano = data.year + (data.month + 1) // 12
            mes = (data.month + 1) % 12
            if mes == 0:
                mes = 12
                ano -= 1       
            dia = min(data.day, (data.replace(month=mes, year=ano) - timedelta(days=1)).day)        
            data_incrementada = data.replace(year=ano, month=mes, day=1)        
            return data_incrementada
    






    
    
    def formatar_data_inicio_mes(data):
        return data.strftime("01/%m/%Y")



    
    def verificar_quinzena(data1):
        return data1.day == 15    

    def mesmo_mes(data1, data2):
        return data1.year == data2.year and data1.month == data2.month

    def mesmo_ano(data1, data2):
        return data1.year == data2.year

    def formato_ano_mes_dia(data_str):
        ''' converte a string 01/07/2023 em 2023-07-01 '''
        partes = data_str.split("/")
        nova_data = f"{partes[2]}-{partes[1]}-{partes[0]}"
        return nova_data

    def formatar_dataobj_para_string_dmy(data_obj):
        ''' converte a data 2023-07-01 00:00:00+0000 em 01/07/2023 '''    
        data_formatada = data_obj.strftime("%d/%m/%Y")
        return data_formatada

    def converter_data_para_str(data_obj):
        ''' converte a data 2023-07-01 00:00:00+0000 em 01/07/2023 '''    
        data_formatada = data_obj.strftime("%d/%m/%Y")
        return data_formatada

    def converter_data_para_str_slim(data_obj):
        data_formatada = data_obj.strftime("%Y-%m-%d")
        return data_formatada


