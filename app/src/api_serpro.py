from src.api_utils import get_api
from src.api_get import *
from src.configura_debug import *
from acd_app.constantes import API_SERPRO

"""Este módulo é responsável por buscar os dados na api-serpro por meio 
   da função get_api() """

class ApiSerpro():

    base_url = API_SERPRO
    
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