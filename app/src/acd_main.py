
from src.api_serpro import ApiSerpro
from src.configura_debug import *
from src.verificacpf import *

from src.acd_manipulacao_extracao import *

from src.acd_classes import Exequente, FichaFinanceira
from src.acd_manipulacao_extracao import ManipulacaoExtracaoRubricas
from src.acd_montagem_ficha_financeira import MontagemFichaFinanceira



def obter_ficha_financeira(lista_cpf_validos,anoi, anof)->dict:
    '''retira a ficha finaceira do exequente e retorna um dicionário
       no formato utilizado para extração de fichas financeiras'''
    dict_fichas = {}
    for cpf in lista_cpf_validos:
        exequente = FichaFinanceira(cpf, anoi, anof)
        iu = exequente.iu
        ficha = exequente.get_ficha_financeira()       
        descricoes_rubricas = exequente.get_codigos_e_descricao_rubricas_extracao()        
        
        montagem_ficha = MontagemFichaFinanceira(descricoes_rubricas)
        fichaformatada = montagem_ficha.criar_dicionario(ficha)
        # inclui uma chave para cada iu de exequente        
        dict_fichas[iu]=fichaformatada
    return dict_fichas
    #info(f"dict_fichas: {dict_fichas}")


def extrair_rubricas(cpf_validos, anoinicial, anofinal, orgao, rubricas):
    livro = []
    for cpf in cpf_validos:
        
        # instancia um exequente desse cpf
        exequente = FichaFinanceira(cpf, anoinicial, anofinal)
        
        # obter o nome do exequente
        nome = exequente.nome        
        
        # obter a extracao de rubricas desse cpf
        extracao = exequente.get_extracao_rubricas()
        
        # obter todos os orgaos e codigos das rubricas da extracao
        orgaos_extracao = exequente.get_vinculos()
        codigos_rubricas_extracao = exequente.get_codigos_rubricas_extracao()
        
        #codigos_rubricas_extracao = ManipulacaoExtracaoRubricas.gerar_lista_codigos_todas_rubricas_extracao(extracao)

        # verificar se é para filtrar pelo órgão        
        if orgao:
            extracao = ManipulacaoExtracaoRubricas.gerar_extracao_filtrada_pelo_orgao(extracao, orgao)
            codigos_rubricas_extracao = ManipulacaoExtracaoRubricas.gerar_lista_de_codigos_rubricas_extracao_filtrada_por_orgao(extracao)
            
        # verificar se é para filtrar pelas rubricas
        #rubricas = list(set([item for item in rubricas if item !=""]))    
        rubricas = sorted(list(filter(bool,rubricas)))    
        
        if len(rubricas) > 0:        
            extracao = ManipulacaoExtracaoRubricas.filtrar_extracao_pelos_codigos_rubricas(extracao, rubricas)

        # selecionar o órgão ou todos os órgãos da extração
        orgaos_lista = [orgao] if orgao else orgaos_extracao        
        # selecionar as rubricas ou todas as rubricas da extração
        rubricas_lista = codigos_rubricas_extracao if len(rubricas) == 0 else rubricas
        lista_orgaos_com_descricao = ManipulacaoExtracaoRubricas.obter_descricao_dos_codigos_orgaos(orgaos_lista)        
        
        agrupadas = ManipulacaoExtracaoRubricas.agrupar_rubricas(extracao, 
                                                                rubricas_lista,
                                                                orgaos_lista,
                                                                anoinicial,
                                                                anofinal,
                                                                nome,
                                                                cpf,
                                                                lista_orgaos_com_descricao)
        '''
        agrupadas = agrupar_rubricas(extracao, 
                                     rubricas_lista, 
                                     orgaos_lista, 
                                     anoinicial, 
                                     anofinal, 
                                     nome, 
                                     cpf,
                                     lista_orgaos_com_descricao)        
        '''
        livro.append(agrupadas)
        lista_rubricas_descricao = ManipulacaoExtracaoRubricas.obter_descricao_dos_codigos_rubricas(rubricas_lista)        
    return livro, lista_rubricas_descricao   


def obter_data_obito(cpf_validos): 
    dict_obitos = []
    for num_id, cpf in enumerate(cpf_validos, start=1):
        exequente = Exequente(cpf)
        cpf = formater(exequente.cpf)
        nome = exequente.nome
        data_obito = exequente.data_obito
        dict_obitos.append({
                'id': num_id,
                'cpf': cpf,
                'nome': nome,
                'data': data_obito})
    return dict_obitos
 
