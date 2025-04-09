from src.configura_debug import *
import csv
#from django.http import JsonResponse

from typing import Optional, List, Dict

class Utils:

    @classmethod
    def encontrar_valores_por_nome(cls, tabelas: list, nome_iam: str, nome_juros: str) -> tuple:
        """
        Encontra o nome das tabelas de IAM e de Juros da lista de tabelas no banco de dados.
        Args.
            tabelas (list): Uma lista de listas, onde cada sublista contém [[..., valor, nome],..[..., valor, nome]]
            nome_iam (str): O nome da tabela de IAM a ser procurada.
            nome_juros (str): O nome da tabela de juros a ser procurada.
        Retorno:
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

    @classmethod
    def extrair_campos(cls, lista_campos: list, primeiros: int, ultimos: int) -> tuple:
        """ recebe a lista dos campos e extrai um dicionário em que as chaves são os campos dos formulários e
            uma lista de dicionários de rubricas do arquivo de extração SICAPE sem o tipo 'N'
            
            valores =
            {   'numprocesso': '20-2324-89/2025',
                'nomeexequente': 'JOHN JONES JAMESSON',
                're': 'União',
                'dtajuizamento': '1995-03-10',
                'dtcitacao': '1997-05-01',
                'dtatualizacao': '1993-01-01',
                'termoinicial': '1998-06-30',
                'termofinalC': '2002-02-28',
                'termofinalF': '2002-02-28',
                'termofinalR': '2002-02-28',
                'pagamento': '100',
                'anoinipgto': '2002-02-28',
                'anofimpagto': '2002-02-28',
                'tabpnep': 'Tabela c.m. cond. geral IPCA-E',
                'tabjuros': 'Juros 0,5% até junho de 2009',
                'verificarObito': 'on',
                'aplicarSELIC': 'on',
                'selicJuros': 'off',
                'linha1': 'ADVOCACIA-GERAL DA UNIÃO',
                'linha2': 'Procuradoria Nacional de Execuções e Precatórios/PGU/AGU',
                'linha3': 'DEPARTAMENTO DE CÁLCULOS E PERÍCIAS',
                'linha4': 'Processo: ',
                'linha5': 'Exequente: ',
                'linha6': 'Ré: União',
                'linha7': 'Data do ajuizamento: ',
                'linha8': 'Data da citação: ',
                'linha9': 'Data de atualização: '
            }
            rubricas = [
                [{'codigo': '9', 'descricao': 'VANT.PESSOAL NOM IDENTIFIC-CLT', 'tipo': 'C'},                  
                  {'codigo': '12', 'descricao': 'ADIC TEMPO SERVICO RM JURIDICO', 'tipo': 'C'},
                  {'codigo': '13', 'descricao': 'ADIC.TEMPO SERVICO LEI 8112/90', 'tipo': 'C'},
                  {'codigo': '15', 'descricao': 'REPRESENTACAO MENSAL', 'tipo': 'F'},
                  {'codigo': '16', 'descricao': 'HORAS SUPLEMENTARES - CLT', 'tipo': 'C'},
                  {'codigo': '18', 'descricao': 'ADIC.TEMPO SERV.L.8112/90-APOS', 'tipo': 'C'},
                ]
            """
        
        def ajustar_lista(resultado: list) -> list:
            """
            Transforma a lista de dicionários no formato:
                [{'codigo_X': 'X'}, {'descricao_X': 'DESCRICAO'}, {'tipo_X': 'TIPO'}, ...]
            no formato:
                [{'codigo': 'X', 'descricao': 'DESCRICAO', 'tipo': 'TIPO'}, ...]
            Args:
                lista_original (list[dict]): Lista de dicionários no formato original.
            Returns:
                list[dict]: Lista de dicionários no formato transformado.
            """            
            resultado_ajustado =[]
            for i in range(0, len(resultado),3):
                codigo_dict = resultado[i]
                descricao_dict = resultado[i + 1]
                tipo_dict = resultado[i + 2]

                tipo_valor = list(tipo_dict.values())[0]
                
                if tipo_valor != 'N':
                    novo_dicionario = {
                        'codigo': list(codigo_dict.values())[0],        # pegar o valor da chave 'codigo_X'
                        'descricao': list(descricao_dict.values())[0],  # pegar o valor da chave 'descricao_X'
                        'tipo': list(tipo_dict.values())[0]             # pegar o valor da chave 'tipo_X'
                        }
                    resultado_ajustado.append(novo_dicionario)                    
            return resultado_ajustado               
        
        primeiros_campos = lista_campos[:primeiros]
        ultimos_campos = lista_campos [-ultimos:]
        valores = {}
        for d in primeiros_campos + ultimos_campos:
            valores.update(d)
        rubricas = ajustar_lista(lista_campos[primeiros:-ultimos])        
        return valores, rubricas
    

    @classmethod
    def filtrar_rendimentos_sicape(cls, arquivo):
        """
        Filtra as linhas do arquivo completo que terminam com ";1".
        Args:
            arquivo (bytes): O conteúdo do arquivo codificado em bytes.
        Returns:
            list[str] | None: Uma lista de strings contendo as linhas filtradas
        """
        try:
            linhas = arquivo.readlines()
            linhas_filtradas = [linha.strip() for linha in linhas if linha.strip().endswith(";1")]
            return linhas_filtradas

        except Exception as e:
            info(f"Erro ao processar o arquivo: {e}")
            return None
        
    @classmethod
    def obter_rubricas_extracao_sicape(cls, linhas_arquivo_filtrado):        
        """
        Extrai valores únicos dos codigos das rubricas, da coluna 4 (índice 3) de uma lista de linhas filtradas.
        Args:
            linhas_arquivo_filtrado (list[str]): Uma lista de strings representando as linhas filtradas.
        Returna:
            list[int] | None: Uma lista ordenada de inteiros contendo os códigos das rubricas
        """
        try:
            valores_coluna4 = set()  
            for linha in linhas_arquivo_filtrado:
                linha = linha.strip()               # Remove espaços em branco e quebras de linha
                if linha and ";" in linha:          # Ignora linhas vazias ou mal formatadas
                    campos = linha.split(";")       # Divide a linha pelo delimitador ";"
                    if len(campos) > 3:             # Garante que a linha tem pelo menos 4 colunas
                        try:
                            valor = int(campos[3])  # Converte o valor da coluna 4 para inteiro, não tem ponto no número
                            valores_coluna4.add(valor)
                        except ValueError:
                            info(f"Valor inválido na coluna 4: {campos[3]}")
            valores_ordenados = sorted(valores_coluna4)            
            return valores_ordenados
        except Exception as e:
            print(f"Erro ao processar o arquivo: {e}")
            return None
        
        
    @classmethod
    def extrair_fitas_sicape(cls, rubricas, lista_extracao):
        listaC = []
        listaF = []
        listaR = []
        listaP = []

        # Iterar sobre a lista de rubricas
        for rubrica in rubricas:
            codigo_com_ponto = rubrica['codigo']
            codigo = codigo_com_ponto.replace('.','') 
            codigo = int(codigo) 
            if codigo in lista_extracao:
                tipo = rubrica['tipo']            
                if tipo == 'C':
                    listaC.append(codigo)
                elif tipo == 'F':
                    listaF.append(codigo)
                elif tipo == 'R':
                    listaR.append(codigo)
                elif tipo == 'P':
                    listaP.append(codigo)
        resultado = {
            'C': listaC,
            'F': listaF,
            'R': listaR,
            'P': listaP
        }
        return resultado
    

    @classmethod
    def processar_arquivo_completo_e_simplificado_sicape(cls, simplificado, linhas_filtradas, rubricas_calculo) -> list:
        """
        Processa os arquivos simplificado e completo para gerar uma lista de dados processados.

        Args:
            simplificado: 
                Arquivo contendo os dados dos executantes no formato simplificado. Espera-se que o arquivo tenha 
                colunas como CODIGO, CPF, IDENTIFICACAO_UNICA, MATRICULA_BENEFICIARIO, NOME e CARGO.

            linhas_filtradas (list[str]): 
                Lista de strings representando as linhas filtradas do arquivo completo. Cada linha deve estar no 
                formato delimitado por ';', contendo informações como CODIGO, CODIGO_ORGAO, ANO_MES, CODIGO_RUBRICA, 
                DESC_RUBRICA, VALOR, etc, mas apenas as que terminam com valor 1.

        Returns:
            list[dict]: 
                Uma lista de dicionários contendo os dados processados. Cada dicionário representa um exequente 
                e suas rubricas associadas.

                Estrutura de cada dicionário:
                - 'iu' (int): Identificação única.
                - 'cpf' (str): CPF.
                - 'nome' (str): Nome.
                - 'matricula' (str): Matrícula.
                - 'beneficiario' (str): Nome beneficiário (se vazio insere '0').
                - 'cargo' (str): Cargo.
                - 'rubricas' (list[dict]): Lista de rubricas da extração.

                Estrutura de cada rubrica:
                - 'codorgao' (int): Código do órgão.
                - 'codrubrica' (int): Código da rubrica.
                - 'datapagto' (str): Data no formato AAAAMM.
                - 'valor' (float): Valor da rubrica.
                - 'descricao' (str): Descrição da rubrica.
        
                 [{'iu': 1823388, 'cpf': '121.191.181-11', 'nome': 'ANTONIO CAVALCANTE', 'matricula': '0', 'beneficiario': '0', 
                    'cargo': '901-1', 
                    'rubricas': []}, ...
                  {'iu': 1837087, 'cpf': '121.121.141-14', 'nome': 'ANTONIO BOTELHO', 'matricula': '0', 'beneficiario': '0', 
                    'cargo': '901-1', 
                    'rubricas': [      
                       {'codorgao': 20115, 'codrubrica': 175, 'datapagto': '199701', 'valor': 17.66, 'descricao': 'LEI 8216 APOS.'}, 
                       {'codorgao': 20115, 'codrubrica': 1087, 'datapagto': '199701', 'valor': 278.93, 'descricao': '902329-7 VENC. DPF'}, 
                       {'codorgao': 20115, 'codrubrica': 1087, 'datapagto': '199701', 'valor': 557.87, 'descricao': '902329-7 VENC. DPF'}, 
                        ... 
                       {'codorgao': 20115, 'codrubrica': 1087, 'datapagto': '199701', 'valor': 446.29, 'descricao': 'AO 902329-7 VENC. DPF'}
                    ]}]                
        """
        rubricas_permitidas = [cod for lista in rubricas_calculo.values() for cod in lista]

        try:
            # Ler o arquivo simplificado (ignorando o cabeçalho)
            leitor_simplificado = csv.reader(simplificado, delimiter=';')
            next(leitor_simplificado)  # Ignora a primeira linha (cabeçalho)

            # Processar o arquivo simplificado para obter a última linha de cada código
            ultimas_linhas = {}
            for linha in leitor_simplificado:
                if len(linha) >= 6:  # Garantir que a linha tem todas as colunas esperadas
                    codigo = linha[0]  # CODIGO está na coluna 0
                    ultimas_linhas[codigo] = {
                        "CODIGO": linha[0],
                        "CPF": linha[1],
                        "IDENTIFICACAO_UNICA": linha[2],
                        "MATRICULA_BENEFICIARIO": linha[3],
                        "NOME": linha[4],
                        "CARGO": linha[5]
                    }

            #info(f"Últimas linhas do arquivo simplificado:\n{ultimas_linhas}") 

            # Criar uma lista de rubricas agrupadas por código
            rubricas_por_codigo = {}
            for linha in linhas_filtradas:
                campos = linha.split(";")
                if len(campos) >= 8:
                    try:
                        codigo = campos[0].strip()  # CODIGO está na coluna 0
                        codorgao = int(campos[1].strip())
                        datapagto = campos[2].strip()
                        codrubrica = int(campos[3].strip())
                        descricao = campos[4].strip()
                        valor = float(campos[6].strip().replace(',','.'))
                    except ValueError as ve:
                        info(f"Linha inválida ignorada: {linha}. Erro{ve}")
                        continue

                    # verificar se a rubrica está na lista de rubricas permitidas
                    if codrubrica not in rubricas_permitidas:
                        continue

                    rubrica = {
                        "codorgao": codorgao,  
                        "codrubrica": codrubrica,  
                        "datapagto": datapagto,  
                        "valor": valor,  
                        "descricao": descricao  
                    }
                    if codigo not in rubricas_por_codigo:
                        rubricas_por_codigo[codigo] = []
                    rubricas_por_codigo[codigo].append(rubrica)            
                 
            #info(f"Rubricas agrupadas por código:\n{rubricas_por_codigo}")

            # Criar a lista de dicionários final
            resultado = []
            for codigo, linha_simplificada in ultimas_linhas.items():
                # Obter as rubricas associadas ao código atual
                rubricas = rubricas_por_codigo.get(codigo, [])  # Retorna [] se o código não existir

                # Montar o dicionário exequente
                exequente = {
                    "iu": int(linha_simplificada['IDENTIFICACAO_UNICA']),
                    "cpf": linha_simplificada['CPF'],
                    "nome": linha_simplificada['NOME'],
                    "matricula": linha_simplificada['MATRICULA_BENEFICIARIO'],  # Considerando MATRICULA como matrícula
                    "beneficiario": linha_simplificada.get('BENFICIARIO', '0'),  # Caso BENFICIARIO não exista
                    "cargo": linha_simplificada['CARGO'],
                    "rubricas": rubricas
                }
                # Adicionar à lista final
                resultado.append(exequente)
            return resultado

        except KeyError as ke:
            info(f"Erro de chave: {ke}. Verifique se as colunas estão corretas.")
            return None
        except Exception as e:
            info(f"Erro ao processar os arquivos: {str(e)}")
            return None



    @classmethod
    def obter_codigos_rubricas_ficha(cls, rubricas: List[Dict]) -> List[int]:
        """
        obtém da ficha financeira todas as rubricas utilizadas 
		retorna uma lista ordenada de códigos únicos de rubricas em que rendimento = 1
        """
        rubricas_unicas = {item['codrubrica'] for item in rubricas if item.get('rendimento') == 1}
        return sorted(rubricas_unicas)

	
    @classmethod
    def filtrar_dados_lista_dicionarios(cls,
                                        data: List[Dict], 
                                        chaves_mantidas: List[str], 
                                        chave_filtro: str, 
                                        valor_filtro: int) -> List[Dict]:
        """
	    Filtra uma lista de dicionários com base em uma condição e mantém apenas as chaves desejadas.
			data: lista de dicionários original.
			chaves_mantidas: lista de chaves a serem mantidas nos dicionários filtrados.
			chave_filtro: chave usada para filtrar os dicionários.
			valor_filtro: valor que a chave de filtro deve ter para incluir o dicionário.        
		"""
        return [
        	 	{key: item[key] for key in chaves_mantidas}
         		for item in data if item.get(chave_filtro) == valor_filtro
     	]
    
    @classmethod
    def obter_descricao_rubricas_sicape(cls, resposta: list) -> dict:
        """
        Processa uma lista de dicionários contendo informações de rubricas e retorna um dicionário
        com códigos de rubrica únicos e suas descrições, das utilizadas no cálculo.
        Args:
            resposta (List[Dict[str, Any]]): Lista de dicionários, onde cada dicionário contém informações
                                            sobre um beneficiário e suas rubricas.
        Returns:
            (Dict[int, str]): Dicionário onde as chaves são códigos de rubrica (int) e os valores são
                            descrições (str), sem repetição e ordenados numericamente.
        """        
        descricao = {}

        # Iterar sobre a lista de dicionários
        for item in resposta:
            for rubrica in item['rubricas']:
                codrubrica = rubrica['codrubrica']
                descricao_rubrica = rubrica['descricao']
                # Adicionar ao dicionário apenas se o código ainda não estiver presente
                if codrubrica not in descricao:
                    descricao[codrubrica] = descricao_rubrica

        # Ordenar o dicionário pelo código de rubrica (chave)
        return dict(sorted(descricao.items()))
    

    @classmethod
    def obter_codigo_por_descricao(cls, lista, descricao):
        """
        Função que recebe uma lista de listas e uma descrição,
        e retorna o código correspondente à descrição.
        :param lista: Lista de listas contendo [id, codigo, descricao].
        :param descricao: A descrição para buscar na lista.
        :return: O código correspondente à descrição ou None se não encontrado.
        """
        for item in lista:
            if item[2] == descricao:  # Verifica se o terceiro elemento é igual à descrição
                return item[1]  # Retorna o segundo elemento (código)
        return None  # Retorna None se a descrição não for encontrada
    

    @classmethod
    def separar_codigos_rubricas_por_tipo(cls, lista_dicionarios):        
        """
        Separa os valores de 'codigo' (convertidos para inteiros) de uma lista de
        dicionários em duas listas, uma para o tipo 'S' e outra para o tipo 'P',
        mantendo a ordem numérica e sem repetições.

        Args:
            lista_dicionarios: Uma lista de dicionários, onde cada dicionário
                            contém as chaves 'codigo' e 'tipo'.

        Returns:
            Uma tupla contendo duas listas:
                - tipo_s: Lista dos valores de 'codigo' (inteiros) para os
                        dicionários com 'tipo' igual a 'S', em ordem numérica
                        e sem repetições.
                - tipo_p: Lista dos valores de 'codigo' (inteiros) para os
                        dicionários com 'tipo' igual a 'P', em ordem numérica
                        e sem repetições.
        """
        codigos_s = set()
        codigos_p = set()

        for item in lista_dicionarios:
            codigo_str = item.get('codigo')
            tipo = item.get('tipo')
            try:
                codigo_int = int(codigo_str.replace('.',''))
                if tipo == 'S':
                    codigos_s.add(codigo_int)
                elif tipo == 'P':
                    codigos_p.add(codigo_int)
            except (ValueError, TypeError):
                # Lidar com casos onde 'codigo' não é um número válido
                print(f"Ignorando código não numérico: '{codigo_str}'")
                continue

        tipoS = sorted(list(codigos_s))
        tipoP = sorted(list(codigos_p))

        return tipoS, tipoP





