from src.api_serpro import ApiSerpro
from src.configura_debug import *


class Exequente:      

    def __init__(self, cpf, anoinicial=None, anofinal=None)->None:

        ''' atribui todas informações cadastrais do exequente
            disponíveis nos métodos do servidor web SERPRO '''
        
        self.cpf = cpf  #cpf
        self.anoinicial = anoinicial
        self.anofinal = anofinal
        dados = self.get_nome()
        self.nome = dados['nome'] # nome
        self.iu = dados['iu']  #iu
        dados = self.get_data_obito()
        self.data_obito = dados['data_de_obito'] if dados else "" # data obito      
        self.vinculos = self.get_vinculos() # vinculos
        self.descricao_vinculos = self.get_descricao_vinculos() # descricao vinculos

    def get_nome(self)->dict:
        '''retorna \n
           {'nome':nome, 'iu':iu, 'cpf':cpf}'''
        dados = ApiSerpro.pesquisar_cpf(self.cpf)        
        return dados    

    def get_data_obito(self)->dict:
        '''retorna \n
           {'nome':dados['nome'], 'dataobito':dados['data_de_obito'], 'cpf':dados['cpf']}'''
        dados = ApiSerpro.pesquisar_data_de_obito(self.cpf)
        return dados

    def get_vinculos(self)->list:
        ''''retorna \n 
            [17000, 40106, ..., 20125]'''        
        dados = ApiSerpro.pesquisar_vinculos(self.cpf, self.anoinicial, self.anofinal)
                
        return sorted(set([j for i in dados for j in i['orgaos']])) if dados else []   
    
        
    def get_descricao_vinculos(self)->list:
         '''retorn \n
            [{'codigo':17000,'nome':'MINISTERIO DA FAZENDA'},...{'codigo':40106,'nome':'ADVOCACIA-GERAL DA UNIAO'}]''' 
         lista = self.get_vinculos()   
         lista_nomes = [
             {**ApiSerpro.obter_nome_orgao(cod_orgao), 'codigo': int(cod_orgao)}
             for cod_orgao in lista
         ]  
         return lista_nomes

    def get_nivel(self):
        pass

    def get_funcao(self):
        pass

 


class FichaFinanceira(Exequente):

    def __init__(self, cpf, anoinicial=None, anofinal=None):
        super().__init__(cpf, anoinicial, anofinal)

    def get_codigos_rubricas_extracao(self):
        data = self.get_extracao_rubricas()
        return sorted(set(item['codrubrica'] for item in data))
    
    def get_codigos_e_descricao_rubricas_extracao(self):
        codigos = self.get_codigos_rubricas_extracao()
        lista = [
             {**ApiSerpro.obter_descricao_rubrica(cod_rubrica), 'codigo': int(cod_rubrica)}
             for cod_rubrica in codigos
                ]
        dicionario = {item['codigo']: item['descricao'] for item in lista}   
        return dicionario          

    def get_extracao_rubricas(self):
         rubricas = ApiSerpro.extrair_rubricas(self.cpf, self.anoinicial, self.anofinal)
         return rubricas
    
    def get_ficha_financeira(self):
         ficha = ApiSerpro.pesquisar_ficha_financeira(self.cpf, self.anoinicial, self.anofinal)        
         return ficha


    # @classmethod
    # def gerar_lista_codigos_todas_rubricas_extracao(cls,lista):
        
    #     codigos = sorted(set(item['codrubrica'] for item in lista))
    #     return [int(codigo) for codigo in codigos]
        
    # @classmethod
    # def gerar_extracao_filtrada_pelo_orgao(cls, extracao, orgao):
    #     orgao_int = int(orgao)
    #     return [i for i in extracao if i['codorgao'] == orgao_int]
    
    # @classmethod
    # def gerar_lista_de_codigos_rubricas_extracao_filtrada_por_orgao(cls, lista):        
    #     codigos = sorted(set(item['codrubrica'] for item in lista))
    #     return [int(codigo) for codigo in codigos]
        
    # @classmethod 
    # def filtrar_extracao_pelos_codigos_rubricas(cls, extracao, lista):
    #     return [i for i in extracao if str(i['codrubrica']) in lista]
    
    
    # @classmethod
    # def obter_descricao_dos_codigos_rubricas(cls, lista):    
    #     lista_rubricas = [
    #         {**Serpro.obter_descricao_rubrica(cod_rubrica), 'codigo': int(cod_rubrica)}
    #         for cod_rubrica in lista
    #     ]    
    #    return lista_rubricas


