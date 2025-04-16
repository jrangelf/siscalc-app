import pandas as pd
from typing import Optional, List, Dict, Tuple

from src.acd_datetools import *
from src.acd_utils import Utils
from src.api_serpro import ApiSerpro


class MatrizSerpro:
    
    @classmethod
    #async def matriz_tresdezessete(cls,
    def matriz_tresdezessete(cls,
                            cpf: str,
                            anoi: int,
                            anof: int,
                            basecalculo: list,
                            basepagamentos: list,
                            termo_inicial: str,
                            orgao: Optional[int]= None) -> Tuple [pd.DataFrame, pd.DataFrame, List]:
      
      #extracao = await cls.obter_rubricas(cpf, anoi, anof, orgao)
      extracao = cls.obter_rubricas(cpf, anoi, anof, orgao)
      dados_cadastrais = cls.obter_dados_cadastrais(cpf)
      
      unicas = Utils.obter_codigos_rubricas_ficha(extracao)
      
      # retirar apenas as que estão na base de cálculo para compor o cabeçalho
      conjunto_base = set(basecalculo+basepagamentos)
      rubricas_cabecalho = [item for item in unicas if item in conjunto_base]
      rubricas_com_descricao = []      
      for rubrica in rubricas_cabecalho:          
          resposta = ApiSerpro.obter_descricao_rubrica(rubrica)
          if resposta and 'descricao' in resposta:
              descricao_trim = resposta['descricao'].strip() if resposta['descricao'] else "N/A"              
              rubricas_com_descricao.append({rubrica: descricao_trim})
          else:              
              rubricas_com_descricao.append({rubrica: "N/A"})
      
      # retirar data, codrubrica e valor da extração de rubricas
      chaves = ['datapagto', 'codrubrica', 'valor']
      rendimentos = Utils.filtrar_dados_lista_dicionarios(extracao, chaves, 'rendimento', 1)
      df_base, df_pagtos = cls.montar_dataframe_rendimentos(rubricas_cabecalho, 
                                                            rendimentos,
                                                            basepagamentos,
                                                            termo_inicial)
      return df_base, df_pagtos, rubricas_com_descricao
   

    @classmethod
    def matriz_tresdezessete_pensionista(cls,
                            cpf: str,
                            anoi: int,
                            anof: int,
                            basecalculo: list,
                            basepagamentos: list,
                            termo_inicial: str,
                            orgao: Optional[int]= None) -> Tuple [pd.DataFrame, pd.DataFrame, List]:
        ...
    
    
    
    @classmethod
    #async def obter_rubricas(cls,
    def obter_rubricas(cls,
                       cpf: str,
                       anoi: int,
                       anof: int,
                       orgao: Optional[int] = None) -> List[Dict]:
		
        """ extrai rubricas da API e filtra por órgão, se fornecido """
        #extracao = await ApiSerpro.get_extrair_rubricas(cpf, anoi, anof)
        extracao = ApiSerpro.get_extrair_rubricas(cpf, anoi, anof)		
        if orgao is not None:
            extracao = [item for item in extracao if item.get('codorgao') == orgao]
        return extracao

    @classmethod
    def obter_dados_cadastrais(cls,
                               cpf:str, 
                               orgao:Optional[int] = None):
        _cpf, iu, nome = ApiSerpro.pesquisar_nome_iu(cpf)
        data_obito = ApiSerpro.obter_data_obito_api(cpf)['data_de_obito']
        info(f"\nnome: {nome}\niu: {iu}\ndata_obito: {data_obito}\n")
        
        
        return nome, iu, data_obito


    @classmethod
    def montar_dataframe_rendimentos(cls,
								  	 cabecalho: list,
									 rendimentos: list,
									 basepagtos: list,
									 termo_inicial: str) -> Tuple [pd.DataFrame, pd.DataFrame]:
		

		# converter a lista de dicionários em um DataFrame
        df = pd.DataFrame(rendimentos)

		# agrupar por 'datapagto' e 'codrubrica', somando os valores
        df_agrupado = df.groupby(['datapagto', 'codrubrica'], as_index=False)['valor'].sum()
		
		# criar um DataFrame pivot com 'datapagto' como índice e 'codrubrica' como colunas
        df_pivot = df_agrupado.pivot(index='datapagto', columns='codrubrica', values='valor')

        # Remover o nome 'codrubrica' das colunas
        df_pivot = df_pivot.rename_axis(columns=None)
		
		# reordenar as colunas para incluir todas as colunas do cabeçalho
        df_pivot = df_pivot.reindex(columns=cabecalho, fill_value=0)
		
		# resetar o índice para que 'datapagto' seja uma coluna
        df_final = df_pivot.reset_index()
		
		# separar a matriz base de pagtos, retira a coluna datapagto e as colunas da base calculo pagtos
        colunas_base_pagtos = [coluna for coluna in basepagtos if coluna in df_final]
        
        if colunas_base_pagtos:
            df2 = df_final[['datapagto'] + colunas_base_pagtos]
            df2 = df2.fillna(0)
            df2['datapagto'] = DateTools.converter_data_serie_ano_mes_datetime(df2, 'datapagto')
            #info(f"DF2:\n\n{df2}")
        else:
            df2 = None

# # Verifica se colunas_base_pagtos é uma lista não vazia
# if isinstance(colunas_base_pagtos, list) and colunas_base_pagtos:
#     # Verifica se df_final existe e contém as colunas necessárias
#     if 'datapagto' in df_final.columns and all(col in df_final.columns for col in colunas_base_pagtos):
#         # Seleciona as colunas desejadas
#         df_selecionado = df_final[['datapagto'] + colunas_base_pagtos]
        
#         # Preenche valores NaN com 0
#         df_selecionado = df_selecionado.fillna(0)
        
#         try:
#             # Converte a coluna 'datapagto' para datetime
#             df_selecionado['datapagto'] = DateTools.converter_data_serie_ano_mes_datetime(df_selecionado, 'datapagto')
#         except Exception as e:
#             info(f"Erro ao converter a coluna 'datapagto': {e}")
#             df_selecionado = None
        
#         # Log das informações do DataFrame resultante
#         if df_selecionado is not None:
#             info(f"DF_SELECIONADO:\n\n{df_selecionado}")
#     else:
#         # Caso df_final não contenha as colunas necessárias
#         info("O DataFrame 'df_final' não contém as colunas necessárias.")
#         df_selecionado = None
# else:
#     # Caso colunas_base_pagtos seja inválida ou vazia
#     info("A lista 'colunas_base_pagtos' está vazia ou não é válida.")
#     df_selecionado = None		

		# separar a matriz base de cálculo
        colunas_base_calculo = [coluna for coluna in df_final.columns if coluna not in basepagtos]
        df1 = df_final[colunas_base_calculo]
        df1 = df1.fillna(0)
		
		# colocar a coluna 1/3 férias na última posição
        coluna_ferias = df1.pop(220)
        df1[220] = coluna_ferias
		
		#calcular 1/3 de férias
        indice_datapagto = df1.columns.get_loc('datapagto')
        indice_ferias = df1.columns.get_loc(220) # coluna da rubrica 220 (1/3 férias)		
        df1.loc[df1[220] !=0, 220] = df1.iloc[:, indice_datapagto + 1: indice_ferias].sum(axis=1) / 3

		# formatar data para timestamp
        df1['datapagto'] = DateTools.converter_data_serie_ano_mes_datetime(df1, 'datapagto')		
		
		# calcular a soma e o décimo terceiro (convencionado em novembro)
        colunas_somar = df1.columns[1:]
        df1['soma'] = df1[colunas_somar].sum(axis=1)
        df1.loc[df1['datapagto'].dt.month == 11, 'soma'] *= 2	
		
		# aplicar pro-rata
        pro_rata = DateTools.calcular_pro_rata(termo_inicial)
        
        if pro_rata < 1:
            data_inicio_calculo = DateTools.converter_string_para_datetime_dia_primeiro(termo_inicial)
            condicao = df1['datapagto'] == data_inicio_calculo
            df1.loc[condicao, 'soma'] *= pro_rata

		# calcular o valor devido
        df1['(%)'] = 0.0317
        df1['valor_devido'] = df1['soma'] * df1['(%)']		

        return df1, df2












    @classmethod
    def montar_dataframe_2886_sicap(cls, ficha, rubricas_calculo):
        
        resultado = []
        
        # Iterar sobre cada funcionário na ficha
        for exequente in ficha:
            cpf = exequente['cpf']
            iu = exequente['iu']
            nome = exequente['nome']
            matricula = exequente['matricula']
            beneficiario = exequente['beneficiario']
            cargo = exequente['cargo']

            # Verificar a data de obito            
            cpf_limpo = cpf.replace(".", "").replace("-", "")
            dt_obito = ApiSerpro.pesquisar_data_de_obito(cpf_limpo)            
            if dt_obito:
                data_obito = dt_obito.get('data_de_obito', '')
                info(f"## data de obito: ##:  {data_obito}")
            
            # Processar as rubricas do funcionário
            dados_por_categoria = {categoria: {} for categoria in rubricas_calculo.keys()}
            
            for rubrica in exequente['rubricas']:
                codrubrica = rubrica['codrubrica']
                datapagto = rubrica['datapagto']
                valor = rubrica['valor']
                
                # Converter datapagto para formato YYYY-MM-DD
                ano = datapagto[:4]
                mes = datapagto[4:]
                data_formatada = f"{ano}-{mes}-01"
                
                # Verificar em qual categoria a rubrica se encaixa
                for categoria, codigos in rubricas_calculo.items():
                    if codrubrica in codigos:
                        # Adicionar ou somar o valor no dicionário da categoria
                        if data_formatada not in dados_por_categoria[categoria]:
                            dados_por_categoria[categoria][data_formatada] = {}
                        if codrubrica not in dados_por_categoria[categoria][data_formatada]:
                            dados_por_categoria[categoria][data_formatada][codrubrica] = 0
                        dados_por_categoria[categoria][data_formatada][codrubrica] += valor
            
            # Criar DataFrames para cada categoria
            dfs = []
            for categoria, dados in dados_por_categoria.items():
                df = pd.DataFrame.from_dict(dados, orient='index').fillna(0)
                df.index.name = 'data'
                df = df.reindex(columns=rubricas_calculo[categoria], fill_value=0)

                # Ordenar o DataFrame pela coluna data
                df = df.sort_index()

                # Resetar o índice e renomear a coluna para 'Mês/Ano'
                df = df.reset_index().rename(columns={'data': 'Mês/Ano'})

                # Remover colunas com todas as linhas iguais a zero
                df = df.loc[:, (df != 0).any(axis=0)]
                
                # Adicionar o dataframe à lista
                dfs.append(df)
            
            # Armazenar o resultado para o exequente
            resultado.append({
                'iu': iu,
                'cpf': cpf,
                'nome': nome,
                'matricula': matricula,
                'beneficiario': beneficiario,
                'cargo': cargo,
                'dataframes': tuple(dfs)  # Tupla com os DataFrames (df_C, df_F, df_R, df_P)
            })
        
        return resultado

    @classmethod
    def processar_dataframe_2886(cls, resultado_df, campos):
        ...
    
    
    @classmethod
    def matriz_2886_sicap(cls,
                          ficha, 
                          descricao_rubricas_calculo, 
                          lista_rubricas_calculo, 
                          campos):
        
        info(f'CAMPOS:\n{campos}')

        #info(f'rubricas_base_2886:\n{rubricas_base_2886}')
        #info(f'arquivo completo rendimentos:\n{linhas_rendimento_arquivo_completo}')

        info(f"lista_rubricas_calculo: {lista_rubricas_calculo}")
        
         # Exibir o resultado
        info(f"descricao:\n{descricao_rubricas_calculo}")

        #info(f"ficha:\n{ficha}")

        resultado_df = cls.montar_dataframe_2886_sicap(ficha, lista_rubricas_calculo)

        #resultado_processado = cls.processar_dataframe_2886(resultado_df, campos)
        
        # deve processar ajustado pro-rata, data-obito, ferias e decimo-terceiro. também
        # incluir as colunas que devem ser repetidas no F e R.

        
        
        #pd.set_option('display.max_rows', None)
        #pd.set_option('display.max_columns', None)
        #pd.set_option("display.float_format", "{:.2f}".format)

        # Exibir os DataFrames
        # Exibir o resultado
        # for exequente in resultado:
        #     info(f"Exequente: {exequente['nome']} (CPF: {exequente['cpf']})")
        #     info("DataFrames:")
        #     for idx, categoria in enumerate(['C', 'F', 'R', 'P']):
        #         info(f"DataFrame {categoria}:")
        #         info(f"\n{exequente['dataframes'][idx]}\n")
        #     info("\n")

        return resultado_df      
        
    
    
    
    
    
    
    
    
    




    
    
    
    
    







"""


# Dados fornecidos (mesmos dados anteriores)
ficha = [
    {
        'iu': 8922020,
        'cpf': '134.927.136-53',
        'nome': 'VERA LUCIA DUARTE',
        'matricula': '0',
        'beneficiario': '0',
        'cargo': '11-3/AIII',
        'rubricas': [
            {'codorgao': 57202, 'codrubrica': 50, 'datapagto': '199301', 'valor': 4080348.0, 'descricao': 'DIFERENCA INDIVIDUAL'},
            {'codorgao': 57202, 'codrubrica': 253, 'datapagto': '199301', 'valor': 557588.46, 'descricao': 'DIFERENCA INDIVIDUAL L.7923/89'},
            {'codorgao': 57202, 'codrubrica': 220, 'datapagto': '199301', 'valor': 2458935.0, 'descricao': 'FERIAS - ADICIONAL 1/3'},
            {'codorgao': 57202, 'codrubrica': 188, 'datapagto': '199301', 'valor': 6545668.0, 'descricao': 'REPR.MENSAL DEC LEI 2333/87 AT’'}
        ]
    },
    {
        'iu': 6545793,
        'cpf': '059.008.327-91',
        'nome': 'WALTER LEITE LEMOS',
        'matricula': '0',
        'beneficiario': '0',
        'cargo': '408-1/SIII',
        'rubricas': [
            {'codorgao': 25000, 'codrubrica': 1, 'datapagto': '199302', 'valor': 6545660.0, 'descricao': 'VENCIMENTO BASICO'},
            {'codorgao': 25000, 'codrubrica': 13, 'datapagto': '199301', 'valor': 4058310.0, 'descricao': 'ANUENIO - ART.244, LEI 8112/90'},
            {'codorgao': 25000, 'codrubrica': 78, 'datapagto': '199301', 'valor': 262910.0, 'descricao': 'PARC INCORPORADA LEI 6732/79'},
            {'codorgao': 25000, 'codrubrica': 188, 'datapagto': '199301', 'valor': 6545660.0, 'descricao': 'REPR.MENSAL DEC LEI 2333/87 AT’'}
        ]
    }
]

rubricas_calculo = {
    'C': [1, 5, 12, 13, 18, 29, 34, 50, 71, 188, 189, 220, 243, 253, 507, 513, 591, 665, 679, 784, 82230],
    'F': [4, 15, 24, 25, 78, 173, 174, 613, 620, 621, 702, 719, 720, 723, 727, 728, 731, 732, 739, 740, 852, 901],
    'R': [240, 241, 246],
    'P': [984, 8030, 10230, 17001, 82175, 82240]
}






import pandas as pd

# Função para criar a estrutura final (mesma função anterior)
def criar_resultado(ficha, rubricas_calculo):
    resultado = []
    
    # Iterar sobre cada funcionário na ficha
    for funcionario in ficha:
        cpf = funcionario['cpf']
        iu = funcionario['iu']
        nome = funcionario['nome']
        matricula = funcionario['matricula']
        beneficiario = funcionario['beneficiario']
        cargo = funcionario['cargo']
        
        # Processar as rubricas do funcionário
        dados_por_categoria = {categoria: {} for categoria in rubricas_calculo.keys()}
        
        for rubrica in funcionario['rubricas']:
            codrubrica = rubrica['codrubrica']
            datapagto = rubrica['datapagto']
            valor = rubrica['valor']
            
            # Converter datapagto para formato YYYY-MM-DD
            ano = datapagto[:4]
            mes = datapagto[4:]
            data_formatada = f"{ano}-{mes}-01"
            
            # Verificar em qual categoria a rubrica se encaixa
            for categoria, codigos in rubricas_calculo.items():
                if codrubrica in codigos:
                    # Adicionar ou somar o valor no dicionário da categoria
                    if data_formatada not in dados_por_categoria[categoria]:
                        dados_por_categoria[categoria][data_formatada] = {}
                    if codrubrica not in dados_por_categoria[categoria][data_formatada]:
                        dados_por_categoria[categoria][data_formatada][codrubrica] = 0
                    dados_por_categoria[categoria][data_formatada][codrubrica] += valor
        
        # Criar DataFrames para cada categoria
        dfs = []
        for categoria, dados in dados_por_categoria.items():
            df = pd.DataFrame.from_dict(dados, orient='index').fillna(0)
            df.index.name = 'data'
            
            # Reindexar para garantir que todas as colunas da categoria estejam presentes
            df = df.reindex(columns=rubricas_calculo[categoria], fill_value=0)
            
            # Ordenar o DataFrame pela coluna data
            df = df.sort_index()
            
            # Resetar o índice e renomear a coluna para 'Mês/Ano'
            df = df.reset_index().rename(columns={'data': 'Mês/Ano'})
            
            # Remover colunas com todas as linhas iguais a zero
            df = df.loc[:, (df != 0).any(axis=0)]
            
            # Adicionar o DataFrame à lista
            dfs.append(df)
        
        # Armazenar o resultado para o funcionário
        resultado.append({
            'iu': iu,
            'cpf': cpf,
            'nome': nome,
            'matricula': matricula,
            'beneficiario': beneficiario,
            'cargo': cargo,
            'dataframes': tuple(dfs)  # Tupla com os DataFrames (df_C, df_F, df_R, df_P)
        })
    
    return resultado


# Função para processar os DataFrames de cada CPF
def processar_dataframes(resultado):
    for funcionario in resultado:
        cpf = funcionario['cpf']
        nome = funcionario['nome']
        dataframes = funcionario['dataframes']  # Tupla com os DataFrames (df_C, df_F, df_R, df_P)
        
        print(f"Processando DataFrames do Funcionário: {nome} (CPF: {cpf})")
        
        # Iterar sobre os DataFrames de cada categoria
        for idx, categoria in enumerate(['C', 'F', 'R', 'P']):
            df = dataframes[idx].copy()  # Usar cópia para evitar modificações diretas
            
            # 1. Adicionar uma coluna 'Soma' com a soma de todas as colunas (exceto 'Mês/Ano')
            if len(df.columns) > 1:  # Garantir que há colunas além de 'Mês/Ano'
                df['Soma'] = df.iloc[:, 1:].sum(axis=1)
            
            # 2. Substituir valores na coluna '220' onde 'Mês/Ano' == '1994-01-01'
            if '220' in df.columns:
                df.loc[df['Mês/Ano'] == '1994-01-01', '220'] = 9999  # Substituir por 9999
            
            # Exibir o DataFrame processado
            print(f"DataFrame {categoria} processado:")
            print(df)
            print("\n")
    
    return resultado

# Criar o resultado inicial
resultado = criar_resultado(ficha, rubricas_calculo)

# Processar os DataFrames
resultado_processado = processar_dataframes(resultado)





"""
