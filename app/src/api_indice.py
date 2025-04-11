from src.api_utils import get_api
from src.acd_constantes import API_INDICE

from src.configura_debug import *

"""Este módulo é responsável por buscar os dados na api-indíces por meio 
   da função get_api() """

class ApiIndice:

    base_url = API_INDICE    
    
    @classmethod
    def get_lista_completa_das_tabelas(cls):    
        # retorna uma lista com as tabelas existentes no banco        
        url=cls.base_url + 'descricao_tabelas'
        data = get_api(url)
        lista = []        
        for i in data:  
            lista.append([i['codigo'], i['descricao'], i['nome'], i['observacao']])
        return lista    
    
    @classmethod
    def get_cod_nome_desc_das_tabelas(cls):        
        url = cls.base_url + 'nome_tabelas'
        data = get_api(url)
        lista = []        
        for i in data:  
            lista.append([i['codigo'], i['nome'], i['descricao']])
        #info(f'lista:\n{lista}')
        return lista
        
    
    @classmethod
    def get_tabela(cls, nome_tabela):
        # retorna uma lista de dicionários com as tuplas da tabela            
        url = cls.base_url + nome_tabela
        return get_api(url)
    

