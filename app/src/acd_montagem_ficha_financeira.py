from src.api_serpro import ApiSerpro

from src.configura_debug import *

class MontagemFichaFinanceira:

    @classmethod
    def __init__(cls, codigos):
        cls.descricao_codigos = codigos
        #info(f"==>{cls.descricao_codigos}")

    @classmethod
    def remover_chave_do_dicionario(cls, data):
        '''retira a chave __values__ do arquivo json proveniente da api'''
        if isinstance(data, list):
            return [cls.remover_chave_do_dicionario(item) for item in data]
        elif isinstance(data, dict):
            if "__values__" in data:
                return {key: cls.remover_chave_do_dicionario(value) for key, value in data["__values__"].items()}
            else:
                return {key: cls.remover_chave_do_dicionario(value) for key, value in data.items()}
        else:
            return data
        
    @classmethod
    def remover_repetidos(cls, lista):
        unique_set = set(map(tuple, lista))
        unique_list = list(map(list, unique_set))
        unique_list.sort()
        return unique_list

    @classmethod
    def insere_pagamentos(cls, lista1, lista2, sufixo):
        for i, item1 in enumerate(lista1):            
            ano1, rubrica1, rend1, seq1 = item1[0], item1[2], item1[4], item1[5]
            item1[6] = [0] * len(sufixo)
            
            for j, item2 in enumerate(lista2):
                ano2, rubrica2, rend2, seq2, ano_mes_inclusao, valor = item2[0], item2[2], item2[4], item2[5], item2[6], item2[7]
                
                if ano2 == ano1 and rubrica2 == rubrica1 and rend2 == rend1 and seq2 == seq1:                                        
                    posicao_inclusao_fita_mes = ano_mes_inclusao - (ano2 * 100) - 1                    
                    # atualizar o valor correto para o mês correspondente
                    item1[6][posicao_inclusao_fita_mes] += float(valor)
        return lista1


    @classmethod
    def consolidar_registros(cls, registros):
		# cria uma lista de registros sem a data e sem o valor pago
        lista_reduzida = [aux[:6] for aux in registros]
        # remove os repetidos e ordena a lista
        lista_ordenada = cls.remover_repetidos(lista_reduzida)
		# insere em cada registro o sufixo com os valores de cada mês
        sufixo = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        for i in range(len(lista_ordenada)):
            lista_ordenada[i].append(sufixo)
        return cls.insere_pagamentos(lista_ordenada,registros, sufixo)


    @classmethod
    def criar_dicionario(cls, ficha_raw):
        # remove do arquivo json a tag "__values__"
        ficha = cls.remover_chave_do_dicionario(ficha_raw)
        quantidade_fichas = len(ficha) if ficha else 0
        registros, cadastros = [], []
        if quantidade_fichas > 0:			
            for i in range(quantidade_fichas):				
                servidor = ficha[i]['nome']
                cpf = ficha[i]['CPF']
                ano = ficha[i]['ano']
                iu = ficha[i]['identificacaoUnica']
                quantidade_vinculos = len(ficha[i]['vinculos']['vinculo'])            
                nomecargo = ''
                for j in range(quantidade_vinculos):
                    codigo_orgao = ficha[i]['vinculos']['vinculo'][j]['codOrgao']
                    matricula = ficha[i]['vinculos']['vinculo'][j]['matricula']
                    codigo_grupo_cargo = ficha[i]['vinculos']['vinculo'][j]['codGrupoCargo']
                    codigo_cargo = ficha[i]['vinculos']['vinculo'][j]['codCargo']
                    classe = ficha[i]['vinculos']['vinculo'][j]['classe']
                    padrao = ficha[i]['vinculos']['vinculo'][j]['padrao']
                    sigla_regime = ficha[i]['vinculos']['vinculo'][j]['siglaRegimeJuridico']				
                    quantidade_itens=len(ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'])
                    
                    try:
                        data = ApiSerpro.obter_nome_orgao(codigo_orgao)
                        nomeorgao = data['nome']
                    except:
                        nomeorgao = 'Não informado'

                    if codigo_cargo != 0 and codigo_grupo_cargo != 0:
                        try:
                            data = ApiSerpro.pesquisar_nome_cargo(codigo_cargo,codigo_grupo_cargo)
                            nomecargo = data['nome']                        
                        except:
                            nomecargo = 'Não informado'
                            
                    cad = {'ano':ano,'orgao':codigo_orgao,'matricula':matricula,'codgcargo':codigo_grupo_cargo,'codcargo':codigo_cargo,'classe':classe,'padrao':padrao,'sigla':sigla_regime,'nomeorgao':nomeorgao,'nomecargo':nomecargo}
                    
                    cadastros.append(cad)
                    nomerubrica = ''
                    for k in range(quantidade_itens):					
                        rubrica = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['codigo']
                        rendimento = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['rendimento']
                        sequencia = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['sequencia']
                        datapgto = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['dataPagamento']
                        valor = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['valor']				
                        try:
                            nomerubrica = cls.descricao_codigos.get(rubrica)                                                    
                        except:
                            nomerubrica = 'N/I'                                            
                        reg = [ano,codigo_orgao, rubrica, nomerubrica, rendimento,sequencia,datapgto,float(valor)]
                        registros.append(reg)
            dados_cadastro = {'iu':iu,'nome':servidor,'registros':cadastros}
        else:
            dados_cadastro = {'iu':'','nome':'','registros':''}            
        registros_meses_consolidados =[]

        # registros_meses_consolidados = Processamento.consolidar_registros(registros)    
        registros_meses_consolidados = cls.consolidar_registros(registros)
        
        dicionario = {'cadastro':dados_cadastro,'lancamentos':registros_meses_consolidados}
        
        return dicionario


'''



'''