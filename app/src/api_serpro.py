from typing import Optional, List, Dict

from src.api_utils import get_api
from src.api_get import *
from src.configura_debug import *
from src.acd_constantes import API_SERPRO

"""Este módulo é responsável por buscar os dados na api-serpro por meio 
   da função get_api() """

class ApiSerpro():

    base_url = API_SERPRO
    
    @classmethod
    def remover_values_key(cls, data):
        '''
        Remove a chave '__values__' de uma estrutura aninhada.
        A estrutura de dados (dicionário ou lista) que pode conter a chave '__values__'.
        '''
        if isinstance(data, dict):  # Se for um dicionário
            if '__values__' in data:
                # Substitui o dicionário pelo valor da chave '__values__'
                return cls.remover_values_key(data['__values__'])
            else:
                # Processa recursivamente cada valor do dicionário
                return {key: cls.remover_values_key(value) for key, value in data.items()}
        elif isinstance(data, list):  # Se for uma lista
            # Processa recursivamente cada elemento da lista
            return [cls.remover_values_key(item) for item in data] 
        else:
            # Retorna o valor diretamente se não for dicionário nem lista
            return data    
    
    @classmethod
    def get_extrair_rubricas(cls, cpf: str, anoi: str, anof: str) -> dict:        
         url = f'{cls.base_url}rubricas/{cpf}?anoinicial={anoi}&anofinal={anof}'         
         data = get_api(url)
         return data


    @classmethod
    def pesquisar_nome_iu(cls, cpf: str) -> tuple:
        # retorna uma lista com as tabelas existentes no banco        
        url=f'{cls.base_url}pesquisarcpf/{cpf}'
        data = get_api(url)
        cpf, nome, iu = data['cpf'], data['iu'], data['nome']               
        return cpf, nome, iu    
    
    @classmethod
    def extrair_ficha_financeira(cls, cpf: str, anoi: str, anof: str) -> list:
         url = f'{cls.base_url}fichafinanceira/{cpf}?anoinicial={anoi}&anofinal={anof}'
         data = get_api(url)
         cleaned_data = cls.remove_values_key(data)
         return cleaned_data 
    
    @classmethod
    def extrair_rubricas_api(cls, cpf: str, anoi: str, anof: str) -> dict:        
         url = f'{cls.base_url}rubricas/{cpf}?anoinicial={anoi}&anofinal={anof}'         
         data = get_api(url)
         return data

        
    @classmethod
    def obter_data_obito_api():
        ...

    @classmethod
    def obter_pensionistas():
        ...

    @classmethod
    def obter_cotaparte():
        ...  

    @staticmethod
    def add_get_api(sufixo: str):        
        url = f"{API_SERPRO}{sufixo}"        
        data = get_api(url)
        return data
    
    @classmethod
    def pesquisar_cpf(cls, cpf: str):
        url = cls.base_url + f'pesquisarcpf/{cpf}'
        data = get_api(url)
        return data

    #trocar os métodos abaixo para utilizar o getapi.
    @classmethod
    def pesquisar_data_de_obito(self, cpf: str):
        sufixo = f"datadeobito/{cpf}"         
        data = self.add_get_api(sufixo)
        return data

    @classmethod
    def extrair_rubricas(self, cpf, anoinicial, anofinal):
        sufixo = f"rubricas/{cpf}?anoinicial={anoinicial}&anofinal={anofinal}"
        data = self.add_get_api(sufixo)
        return data

    @classmethod
    def obter_descricao_rubrica(self, codigo):        
        sufixo = f"descricaorubrica/?codigo={codigo}"
        data = self.add_get_api(sufixo)
        return data

    @classmethod
    def obter_nome_orgao(self, codigo):
        sufixo = f"nomeorgao/?codigo={codigo}"
        data = self.add_get_api(sufixo)
        return data

    @classmethod
    def pesquisar_ficha_financeira(self, cpf, anoinicial, anofinal):        
        sufixo = f"fichafinanceira/{cpf}?anoinicial={anoinicial}&anofinal={anofinal}"
        data = self.add_get_api(sufixo)
        return data
    
    @classmethod
    def pesquisar_nome_cargo(self, codcargo, codgrupo):        
        sufixo = f"cargoemprego/?codcargo={codcargo}&codgrupo={codgrupo}"
        data = self.add_get_api(sufixo)
        return data
    
    @classmethod
    def pesquisar_vinculos(self, cpf, anoinicial, anofinal):        
        sufixo = f"vinculos/{cpf}?anoinicial={anoinicial}&anofinal={anofinal}"
        data = self.add_get_api(sufixo)
        return data