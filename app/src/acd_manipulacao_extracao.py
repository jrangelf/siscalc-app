from src.api_serpro import ApiSerpro
from src.configura_debug import *

class ManipulacaoExtracaoRubricas:

    @staticmethod
    def gerar_periodo(anoi, anof):
        anof = int(anof)
        anoi = int(anoi)
        return [(item * 100) + mes for item in range(anoi, anof+1) for mes in range(1, 13)]

    @classmethod
    def calcular_soma_valores(cls, itens):
        soma = sum(float(item['valor']) for item in itens)
        return soma

    @classmethod
    def gerar_lista_codigos_todas_rubricas_extracao(cls,lista):
        
        codigos = sorted(set(item['codrubrica'] for item in lista))
        return [int(codigo) for codigo in codigos]
        
    @classmethod
    def gerar_extracao_filtrada_pelo_orgao(cls, extracao, orgao):
        orgao_int = int(orgao)
        return [i for i in extracao if i['codorgao'] == orgao_int]
    
    @classmethod
    def gerar_lista_de_codigos_rubricas_extracao_filtrada_por_orgao(cls, lista):        
        codigos = sorted(set(item['codrubrica'] for item in lista))
        return [int(codigo) for codigo in codigos]
        
    @classmethod 
    def filtrar_extracao_pelos_codigos_rubricas(cls, extracao, lista):
        return [i for i in extracao if str(i['codrubrica']) in lista]
    
    @classmethod
    def obter_descricao_dos_codigos_orgaos(cls, lista):        
        try:
            lista_nomes = [
            {**ApiSerpro.obter_nome_orgao(cod_orgao), 'codigo': int(cod_orgao)}
            for cod_orgao in lista
            ]
        except:
            lista_nomes =[]  
        return lista_nomes

    @classmethod
    def obter_descricao_dos_codigos_rubricas(cls, lista):
        try:
            lista_rubricas = [
            {**ApiSerpro.obter_descricao_rubrica(cod_rubrica), 'codigo': int(cod_rubrica)}
            for cod_rubrica in lista
            ]
        except:
            lista_rubricas = [
            {'descricao':'N/C', 'codigo': int(cod_rubrica)}
            for cod_rubrica in lista
            ]    
        return lista_rubricas
    
    @classmethod
    def agrupar_rubricas(cls, extracao, rubricas, orgaos, anoi, anof, nome, cpf, descricao_orgaos):
        periodo = ManipulacaoExtracaoRubricas.gerar_periodo(anoi, anof)        
        agrupadas = []
        orgao_dict = {} 

        for orgao in orgaos:
            descricao = 'N/I'
            for item in descricao_orgaos:
                    
                if int(orgao) == int(item['codigo']):
                    descricao = item['nome']
            
            orgao_int = int(orgao)
            orgao_dict['cpf'] = cpf
            orgao_dict['nome'] = nome
            orgao_dict['codorgao'] = orgao_int
            orgao_dict['nomeorgao'] = descricao 
            
            data_dict = {}
            datas = []

            for anomes in periodo:
                anomes_int = int(str(anomes)) # itera a lista do período ['200801','200802'...'202012']
                ingressos = []            

                for codrubrica in rubricas: # itera a lista das rubricas ['1','18'...'87543']
                    codrubrica_int = int(codrubrica)

                    # gera o dicionário item como resultado das buscas em receitas e e despesas

                    receitas = [item for item in extracao if item['codorgao'] == orgao_int and 
                                                        item['datapagto'] == anomes_int and
                                                        item['codrubrica'] == codrubrica_int and
                                                        item['rendimento'] == 1]
                    
                    descontos = [item for item in extracao if item['codorgao'] == orgao_int and 
                                                        item['datapagto'] == anomes_int and
                                                        item['codrubrica'] == codrubrica_int and
                                                        item['rendimento'] == 2]
                    
                    rubricas_dict ={}
                    if receitas:                    
                        if len(receitas) == 1: # não há "duplicadas" no mesmo mês                                        
                            rubricas_dict['codrubrica'] = codrubrica_int                    
                            rubricas_dict['R'] = receitas[0]['valor']
                            receitas = []
                            receitas.append(rubricas_dict)
                        elif len(receitas) > 1:
                            soma = cls.calcular_soma_valores(receitas)
                            receitas = []                    
                            rubricas_dict['codrubrica'] = codrubrica_int
                            rubricas_dict['R'] = soma
                            receitas.append(rubricas_dict)

                    if descontos:
                        if len(descontos) == 1:
                            rubricas_dict['codrubrica'] = codrubrica_int                    
                            rubricas_dict['D'] = descontos[0]['valor']
                            descontos = []
                            descontos.append(rubricas_dict)
                        elif len(descontos) > 1:                    
                            soma = cls.calcular_soma_valores(descontos)
                            descontos = []                    
                            rubricas_dict['codrubrica'] = codrubrica_int                    
                            rubricas_dict['D'] = soma                    
                            descontos.append(rubricas_dict)                        

                    if rubricas_dict:
                        ingressos.append(rubricas_dict)
                                            
                data_dict['datapagto']=anomes_int
                data_dict['ingressos']=ingressos

                datas.append(data_dict)
                data_dict = {}

            orgao_dict['datas'] = datas
            datas = []

            agrupadas.append(orgao_dict)
            orgao_dict ={}       
                    
        return agrupadas


    