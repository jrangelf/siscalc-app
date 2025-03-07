from src.configura_debug import *




class Utils:


    @classmethod
    def encontrar_valores_por_nome(cls, tabelas: list, nome_iam: str, nome_juros: str) -> tuple:
        """
        Encontra o nome das tabelas de IAM e de Juros da lista de tabelas no banco de dados.

        entrada:
            tabelas (list): Uma lista de listas, onde cada sublista contém [[..., valor, nome],..[..., valor, nome]]
            nome_iam (str): O nome da tabela de IAM a ser procurada.
            nome_juros (str): O nome da tabela de juros a ser procurada.
        saída:
            uma tupla contendo os nomes das tabelas de IAM e de juros.
        erro:
            TypeError: Se a entrada não for do tipo esperado.
        """

        if not isinstance(tabelas, list) or not all(isinstance(tabela, list) for tabela in tabelas):
            raise TypeError("A entrada 'tabelas' deve ser uma lista de listas.")

        if not isinstance(nome_iam, str) or not isinstance(nome_juros, str):
            raise TypeError("Os nomes devem ser strings.")

        valor_iam = None
        valor_juros = None

        for tabela in tabelas:
            if len(tabela) >= 3:  # a sublista tem pelo menos 3 elementos
                nome = tabela[2]
                valor = tabela[1]

                if nome == nome_iam:
                    valor_iam = valor
                elif nome == nome_juros:
                    valor_juros = valor

                if valor_iam is not None and valor_juros is not None:
                    return valor_iam, valor_juros  # Retorno antecipado

        return valor_iam, valor_juros








"""

'''

def converter_tipo1_to_tipo2(data)->dict:
    '''retira do arquivo json a tag __values__'''
    if isinstance(data, list):
        return [converter_tipo1_to_tipo2(item) for item in data]
    elif isinstance(data, dict):
        if "__values__" in data:
            return {key: converter_tipo1_to_tipo2(value) for key, value in data["__values__"].items()}
        else:
            return {key: converter_tipo1_to_tipo2(value) for key, value in data.items()}
    else:
        return data


def montar_ficha_financeira(ficha):

    info("->(formata ficha financeira-begin)<----------")

    quantidade_fichas = len(ficha) if ficha else 0
    registros, cadastros = [], []
    if quantidade_fichas > 0:			
        for i in range(quantidade_fichas):				
            servidor = ficha[i]['nome']
            cpf = ficha[i]['CPF']
            ano = ficha[i]['ano']
            iu = ficha[i]['identificacaoUnica']
            quantidade_vinculos = len(ficha[i]['vinculos']['vinculo'])            
            # iterar por cada vínvulo
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
                    data = Serpro.obter_nome_orgao(codigo_orgao)
                    nomeorgao = data['nome']
                except:
                    nomeorgao = 'Não informado'

                if codigo_cargo != 0 and codigo_grupo_cargo != 0:
                    try:
                        data = Serpro.pesquisar_nome_cargo(codigo_cargo,codigo_grupo_cargo)
                        nomecargo = data['nome']                        
                    except:
                        nomecargo = 'Não informado'
                        
                cad = {'ano':ano,'orgao':codigo_orgao,'matricula':matricula,'codgcargo':codigo_grupo_cargo,'codcargo':codigo_cargo,'classe':classe,'padrao':padrao,'sigla':sigla_regime,'nomeorgao':nomeorgao,'nomecargo':nomecargo}
                info(f"cad: {cad}")
                cadastros.append(cad)
                nomerubrica = ''
                for k in range(quantidade_itens):					
                    rubrica = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['codigo']
                    rendimento = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['rendimento']
                    sequencia = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['sequencia']
                    datapgto = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['dataPagamento']
                    valor = ficha[i]['vinculos']['vinculo'][j]['fichaFinanceira']['itemFichaFinanceira'][k]['valor']				
                    try:
                        lista = [rubrica]
                        dados = ManipulaExtracao.obter_descricao_dos_codigos_rubricas(lista)                        
                        nomerubrica = dados[0]['descricao']                        
                    except:
                        nomerubrica = 'N/I'
										
                    reg = [ano,codigo_orgao, rubrica, nomerubrica, rendimento,sequencia,datapgto,float(valor)]
                    registros.append(reg)

        dados_cadastro = {'iu':iu,'nome':servidor,'registros':cadastros}
    else:
        dados_cadastro = {'iu':'','nome':'','registros':''}
		
    registros_meses_consolidados =[]

    # registros_meses_consolidados = Processamento.consolidar_registros(registros)    
    registros_meses_consolidados = consolidar_registros(registros)
    dicionario = {'cadastro':dados_cadastro,'lancamentos':registros_meses_consolidados}    
    info("->(formata ficha financeira-end)<--")    
    return dicionario


def agrupar_rubricas(extracao, rubricas, orgaos, anoi, anof, nome, cpf, descricao_orgaos):

    #info (f"\nrubricas no agrupamento: {rubricas}\ndescricao orgaos: {descricao_orgaos}")   

    periodo = gerar_periodo(anoi, anof)

    #periodo = [(item * 100) + mes for item in range(anoi, anof+1) for mes in range(1, 13)]
    
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
                
                #término da primeira rubrica
                rubricas_dict ={}
                if receitas:                    
                    if len(receitas) == 1: # não há "duplicadas" no mesmo mês                                        
                        rubricas_dict['codrubrica'] = codrubrica_int                    
                        rubricas_dict['R'] = receitas[0]['valor']
                        receitas = []
                        receitas.append(rubricas_dict)
                    elif len(receitas) > 1:
                        soma = calcular_soma_valores(receitas)
                        receitas = []                    
                        rubricas_dict['codrubrica'] = codrubrica_int
                        rubricas_dict['R'] = soma
                        receitas.append(rubricas_dict)                    
                    #info(f"data: {anomes_int} depois: {receitas}")

                if descontos:
                    if len(descontos) == 1:
                        rubricas_dict['codrubrica'] = codrubrica_int                    
                        rubricas_dict['D'] = descontos[0]['valor']
                        descontos = []
                        descontos.append(rubricas_dict)
                    elif len(descontos) > 1:                    
                        soma = calcular_soma_valores(descontos)
                        descontos = []                    
                        rubricas_dict['codrubrica'] = codrubrica_int                    
                        rubricas_dict['D'] = soma                    
                        descontos.append(rubricas_dict)
                    #info(f"data: {anomes_int} depois: {descontos}")

                if rubricas_dict:
                    ingressos.append(rubricas_dict)
            
            # témino da lista das rubricas
            #info("-------------------------------------------------")
                        
            data_dict['datapagto']=anomes_int
            data_dict['ingressos']=ingressos

            datas.append(data_dict)
            data_dict = {}

        #info(f"datas: {datas}")
        
        # término da lista do período
        orgao_dict['datas'] = datas
        datas = []

        agrupadas.append(orgao_dict)
        orgao_dict ={}
    
    # témino da lista de órgãos
    #info(f"agrupadas: {agrupadas}")        
        
    return agrupadas








#*************************************************************************************

def calcular_soma_valores(itens):
    soma = sum(float(item['valor']) for item in itens)
    return soma


def gerar_lista_mesano(anoi, anof):        
    mesano = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
    lista_mesano = []
    for ano in range(anoi, anof+1): 
        for mes in mesano:
            lista_mesano.append(f'{mes}/{ano}')
    return lista_mesano    


def gerar_periodo(anoi, anof):
    anof = int(anof)
    anoi = int(anoi)
    return [(item * 100) + mes for item in range(anoi, anof+1) for mes in range(1, 13)]


def converter_formato_mes_ano(valor):
        ano = str(valor)[:4]
        mes = str(valor)[4:]
        return '{}/{}'.format(mes, ano)

'''
"""



"""
	deve retornar um dicionário da seguinte forma:
			
	fichas={	IU1 : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}},
				IU2 : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}},
	 			...
	 			IUn : {'cadastro:{ dados_cadastro }, 'registros':{ lancamentos}
	 		}
	dados_cadastro={ {'iu':1234, 'nome':"joaquim", 
					   registros[{ 'ano':1992,
					   				'orgao':123,
					   				'matricula':123,
					   				'codgcargo':12,
					   				'codcargo':22, 
					   				'classe':'C', 
					   				'padrao': 'VI', 
					   				sigla: 'EST'}, {...},{...}
					   			]
	lancamentos=[
					[1992, 25000, 1, 1, 0, [0, 0, 0, 0, 0, 938364.73, 938364.73, 938364.73, 1126037.67, 2506028.98, 2506028.98, 2506028.98]], 
					[1992, 25000, 13, 1, 0, [0, 0, 0, 0, 0, 9383.64, 9383.64, 9383.64, 11260.37, 25060.28, 25060.28, 50120.57]], 
					[1992, 25000, 53, 1, 1, [0, 0, 0, 0, 0, 93836.47, 9383.64, 9383.64, 11260.37, 25060.28, 25060.28, 25060.28]], 
					[1992, 25000, 92, 1, 0, [0, 0, 0, 0, 0, 4044.39, 4044.36, 4044.36, 4853.52, 4853.22, 4853.22, 4853.22]], 
					[1992, 25000, 224, 1, 1, [0, 0, 0, 0, 0, 637866.04, 637866.04, 637866.04, 637866.04, 0, 0, 0]], 
					[1992, 25000, 591, 1, 0, [0, 0, 0, 0, 0, 0, 0, 0, 337811.3, 751808.69, 2004823.18, 2004823.18]],
				]	

"""

"""
exequentes:
[
{'cpf':'23456732987', 'agrupadas':[]},
{'cpf':'87867398732', 'agrupadas':[]
]

agrupadas = [
{'codorgao': 17000, 'datas': [{'datapagto': 200801, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2030.16}]},
				               {'datapagto': 200802, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200803, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200804, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200805, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
                               {'datapagto': 200806, 'ingressos': []},
                               {'datapagto': 200807, 'ingressos': []},
                                                 .
                                                 .
                                                 .
                               {'datapagto': 200910, 'ingressos': []},
                               {'datapagto': 200911, 'ingressos': []},
                               {'datapagto': 200912, 'ingressos': []}]}]                                                         

                                          

exequentes = [{exequente_dict}, {exequente_dict},....,{exequente_dict}]
exequente_dict = {'cpf': '23413463401', 'orgaos': orgaos_lista}

agrupadas = [{orgao_dict},...{orgao_dict}]
orgao_dict = {'codorgao':22000, 'datas': datas}

datas = [{data_dict}, {data_dict},...{data_dict}]
data_dict = {'datapagto':200801, 'ingressos': ingressos}

ingressos = [{rubricas_dict},{rubricas_dict}...{rubricas_dict}]
rubricas_dict = {'codrubrica':13, 'R': 234.23, 'D':125.22}

"""




"""
    Mover a declaração de abater para dentro do loop interno: 
    Atualmente, você declara o dicionário abater fora dos loops 
    e o reutiliza em cada iteração. Isso faz com que todos os 
    elementos em abatimentos sejam referências ao mesmo dicionário. 
    Para corrigir isso, você deve declarar abater dentro do loop 
    interno para criar um novo dicionário em cada iteração. 
    Aqui está um exemplo:

    def gerar_lista_descontos(lista):
        abatimentos = []
        for i in lista:
            for j in i['ficha']:
                if j['rendimento'] == 2 and len(j['rubricas']) != 0:
                    abater = {
                        'orgao': i['orgao'],
                        'data': j['data'],
                        'descontos': j['rubricas']
                    }
                    abatimentos.append(abater)
        return abatimentos

    Utilizar list comprehension: Você também pode usar 
    list comprehension para simplificar o código e evitar 
    o uso explícito de loops. Aqui está um exemplo:

    def gerar_lista_descontos(lista):
        return [
            {
                'orgao': i['orgao'],
                'data': j['data'],
                'descontos': j['rubricas']
            }
            for i in lista
            for j in i['ficha']
            if j['rendimento'] == 2 and len(j['rubricas']) != 0
        ]

        




    
    
    
    
    
"""
    
