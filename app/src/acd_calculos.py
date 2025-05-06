from typing import List, Optional, Tuple

from src.acd_api_serpro import MatrizSerpro
from src.acd_api_indices import MatrizIndices
from src.acd_indices_calculo import Tabelas
from src.acd_serpro_calculo import TabelasSerpro

from src.configura_debug import *
from src.acd_datetools import *
from src.api_indice import *
from src.acd_utils import *

from src.acd_dataframes import DataframeAjustes
from src.api_serpro import ApiSerpro

import pandas as pd


class CalculoSerpro317:
    def __init__(self,
                 anoi: int,
                 anof: int,
                 basecalculo: List[str],
                 basepgtos: List[str],
                 termo_inicial: str,
                 termo_final: str,
                 data_citacao: str,
                 data_atualizacao: str,
                 percentual: int,
                 orgao: Optional[int] = None):
        
        self.anoi = anoi
        self.anof = anof
        self.basecalculo = basecalculo
        self.basepgtos = basepgtos
        self.termo_inicial = termo_inicial
        self.termo_final = termo_final
        self.data_citacao = data_citacao
        self.data_atualizacao = data_atualizacao
        self.percentual = percentual
        self.orgao = orgao

    #async def tabela_para_cpf(self, cpf: str, pensionista: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
    def tabela_para_cpf(self, cpf: str, pensionista: bool = False) -> Tuple[pd.DataFrame, pd.DataFrame, List[str]]:
        """ Monta a tabela do cálculo apenas para o CPF informado. """
        #return await TabelasSerpro.tabelaTresDezessete(
        df_calculo, df_pagamentos, rubricas_cabecalho = TabelasSerpro.tabelaTresDezessete(
                                                        cpf=cpf,
                                                        anoi=self.anoi,
                                                        anof=self.anof,
                                                        basecalculo=self.basecalculo,
                                                        basepgtos=self.basepgtos,
                                                        termo_inicial=self.termo_inicial,
                                                        termo_final=self.termo_final,
                                                        data_citacao=self.data_citacao,
                                                        data_atualizacao=self.data_atualizacao,
                                                        percentual=self.percentual,
                                                        orgao=self.orgao,
                                                        pensionista=pensionista
                                                    )
        return df_calculo, df_pagamentos, rubricas_cabecalho


class Calculos:

    @classmethod
    #async def calcular_317(cls,
    def calcular_317(cls,
                     dict_formularios,
                     ativos,
                     pensionistas):

        campos, rubricas = Utils.extrair_campos(dict_formularios, primeiros=19, ultimos=9)

        anoinipagto = campos.get('anoinipagto','2002')
        anofimpagto = campos.get('anofimpagto','2009')        
        anoInicio = int(campos.get('termoinicial', '1993-01-01').split('-')[0])        
        anoFinal = int(anofimpagto)

        basecalculo, basepagtos = Utils.separar_codigos_rubricas_por_tipo(rubricas)        

        termoInicial = campos.get('termoinicial')
        termoInicial = DateTools.converter_ano_mes_dia_para_string(termoInicial)                       
        termoFinal = campos.get('termofinal')
        termoFinal = DateTools.converter_ano_mes_dia_para_string(termoFinal)
        termoFinalExtendido = '31/12/'+str(anoFinal)

        dataCitacao = campos.get('dtcitacao')
        dataCitacao = DateTools.converter_ano_mes_dia_para_string(dataCitacao)                         
        dataAtualizacao = campos.get('dtatualizacao')
        dataAtualizacao = DateTools.converter_ano_mes_dia_para_string(dataAtualizacao)

        percentual = campos.get('pagamento')
        orgao = campos.get('orgao', None)        
        
        tabpnep = campos.get('tabpnep')
        tabjuros = campos.get('tabjuros')
        
        verificarObito = campos.get('verificarObito')
        verificarObito = {'on': True, 'off': False}.get(verificarObito, None)        
        
        aplicarSELIC = campos.get('aplicarSELIC')
        aplicarSELIC = {'on': True, 'off': False}.get(aplicarSELIC, None)
        
        selicJuros = campos.get('selicJuros')
        selicJuros = {'on': True, 'off': False}.get(selicJuros, None)
        
        lista_tabelas = ApiIndice.get_cod_nome_desc_das_tabelas()
        tabela_pnep = Utils.obter_codigo_por_descricao(lista_tabelas, tabpnep)
        tabela_juros = Utils.obter_codigo_por_descricao(lista_tabelas, tabjuros)

        varios_cpf_ativos = campos.get('varios_cpf_ativo', '')
        varios_cpf_pensionistas = campos.get('varios_cpf_pensionista', '')
        
        cpfs_ativos = [cpf.strip() for cpf in varios_cpf_ativos.split('\n') if cpf.strip()]
        # verificar a validade da lista de cpfs.


        info(f"cpf_ativos:\n{cpfs_ativos}")
        # separar os cpfs inválidos
  
          
        # info(f"[   campos   ]\n{campos}")
        # info(f"[   rubricas   ]\n{rubricas}")
        # info(f"TERMO FINAL EXTENDIDO:{termoFinalExtendido}")
        # info(f"anoInicio:       {anoInicio}")
        # info(f"anoFinal:        {anoFinal}")
        # info(f"basecalculo:     {basecalculo}")
        # info(f"basepagtos:      {basepagtos}")
        # info(f"termoInicial:    {termoInicial}")
        # info(f"termoFinal:      {termoFinal}")
        # info(f"dataCitacao:     {dataCitacao}")
        # info(f"dataAtualizacao: {dataAtualizacao}")
        # info(f"percentual:      {percentual}")
        # info(f"anoinipagto:     {anoinipagto}")
        # info(f"anofimpagto:     {anofimpagto}")
        # info(f"orgao:{orgao}")
        # #info(f"tabpnep:{tabpnep}")
        # #info(f"tabjuros:{tabjuros}")

        # info(f"verificarObito:  {verificarObito}")
        # info(f"aplicarSELIC:    {aplicarSELIC}")
        # info(f"selicJuros:      {selicJuros}")        
        # info(f"tabela_pnep:     {tabela_pnep}")
        # info(f"tabela_juros:    {tabela_juros}")
        
        
        
        
        
        # dados usados para teste:
        #cpf = '24733830904' # luis carlos de assuncao
        cpf = '48662267653'
        #cpf = '19459696449'
  

        # montar o sufixo conforme os dados do cálculo
        tabela = Tabelas(tabela_juros, tabela_pnep, dataCitacao, dataAtualizacao, termoInicial, termoFinalExtendido, aplicarSELIC, selicJuros)
        sufixo = tabela.sufixo()

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option("display.float_format", "{:.2f}".format)

        # instancia o objeto calculador com os dados do cálculo
        calculador = CalculoSerpro317(anoInicio,
                                      anoFinal,
                                      basecalculo,
                                      basepagtos,
                                      termoInicial,
                                      termoFinal,
                                      dataCitacao,
                                      dataAtualizacao,
                                      percentual,
                                      orgao)

        # #basecalculo, basepagtos, rubricas = await calculador.tabela_para_cpf(cpf)
        # basecalculo, basepagtos, rubricas = calculador.tabela_para_cpf(cpf)


        # basepagtos_sufixo = DataframeAjustes.ajustar_df_basepagtos(basepagtos=basepagtos, 
        #                                                            sufixo=sufixo, 
        #                                                            aplicarSELIC=aplicarSELIC,
        #                                                            selicJuros=selicJuros, 
        #                                                            percentual=percentual)
        
                
        # basecalculo_sufixo = DataframeAjustes.ajustar_df_basecalculo(basecalculo=basecalculo, 
        #                                                             sufixo=sufixo, 
        #                                                             aplicarSELIC=aplicarSELIC,
        #                                                             selicJuros=selicJuros)
        

        
        # Executando para cada CPF
        calculos = {}
        nao_processados = {}
        consolidado = {}
        descricao_acumulada_rubricas = {}        

        for cpf in cpfs_ativos:
            try:
                info(f"Calculando para CPF: {cpf}")
                
                '''aqui deve ser verificada a validade do cpf'''

                #cabecalho_exequente = montar_cabecalho_ativo()
                df_basecalculo, df_basepagtos, rubricas_cabecalho = calculador.tabela_para_cpf(cpf) # chama TabelasSerpro.tabelaTresDezessete(..)
                
                descricao_rubricas = {}              

                for rubrica in rubricas_cabecalho:                              
                    if rubrica not in descricao_acumulada_rubricas:
                        resposta = ApiSerpro.obter_descricao_rubrica(rubrica)
                        if resposta and 'descricao' in resposta:
                            #descricao_trim = resposta['descricao'].strip() if resposta['descricao'] else "N/A"
                            descricao_trim = f"{resposta['descricao'].strip()} ({rubrica})" if resposta['descricao'] else f"N/A ({rubrica})"              
                            descricao_acumulada_rubricas[rubrica] = descricao_trim
                        else:              
                            descricao_acumulada_rubricas[rubrica] = "N/A"
                    descricao_rubricas[rubrica] = descricao_acumulada_rubricas[rubrica]                
                
                info(f"\n(1) descricao_rubricas:\n{descricao_rubricas}")                              
               

                basepagtos_com_sufixo = DataframeAjustes.ajustar_df_basepagtos(basepagtos=df_basepagtos, 
                                                                   sufixo=sufixo, 
                                                                   aplicarSELIC=aplicarSELIC,
                                                                   selicJuros=selicJuros, 
                                                                   percentual=percentual,
                                                                   descricao=descricao_rubricas)
                #info(f"basepagtos:\n\n{basepagtos_com_sufixo}")
        
                
                basecalculo_com_sufixo = DataframeAjustes.ajustar_df_basecalculo(basecalculo=df_basecalculo, 
                                                                            sufixo=sufixo, 
                                                                            aplicarSELIC=aplicarSELIC,
                                                                            selicJuros=selicJuros,
                                                                            descricao=descricao_rubricas)
                        
                #info(f"BASE DE CÁLCULO:\n\n{basecalculo_com_sufixo}")
                
                # basecalculo_sufixo['(%)'] = basecalculo_sufixo['(%)'] * 100
                # basecalculo_sufixo['TAXA SELIC (EC 113/2021)']= basecalculo_sufixo['TAXA SELIC (EC 113/2021)']* 100
                # basepagtos_sufixo['TAXA SELIC (EC 113/2021)']= basepagtos_sufixo['TAXA SELIC (EC 113/2021)'] *100
                # 
                # aqui pode substituir o 1995-07-01 por 07/1995 
                

                calculos[cpf] = {                    
                    'pagamentos': basepagtos_com_sufixo,    # Primeiro DataFrame
                    'calculo317': basecalculo_com_sufixo   # Segundo DataFrame
                                    
                }
                
            except Exception as e:
                info(f"\nErro ao calcular para CPF {cpf}: {e}")
                nao_processados[cpf] = None        

        # info(f"nao calculados:{nao_processados}")
        #info(f"calculos:\n\n{calculos}")

        
        return calculos    

# # Executando para cada CPF
# resultados = {}
# for cpf in cpfs:
#     try:
#         print(f"Calculando para CPF: {cpf}")
#         resultado = calculadora.calcular_para_cpf(cpf)
#         resultados[cpf] = resultado
#     except Exception as e:
#         print(f"Erro ao calcular para CPF {cpf}: {e}")
#         resultados[cpf] = None













    @classmethod
    def calcular_2886_sicape(cls,
                             simplificado,
                             completo,
                             dict_formularios):
        
        chaves_desejadas = {
                            'dtajuizamento', 
                            'dtcitacao', 
                            'dtatualizacao', 
                            'dtiniciocalculo', 
                            'termofinalC', 
                            'termofinalF', 
                            'termofinalR', 
                            'pagamento', 
                            'anoinipagto', 
                            'anofimpagto', 
                            'tabpnep', 
                            'tabjuros', 
                            'verificarObito', 
                            'aplicarSELIC', 
                            'selicJuros'
                        }
        
        
        # Dicionário para armazenar os valores encontrados
        valores_encontrados = {}

        # Iterar pela lista até encontrar todas as chaves desejadas
        for item in dict_formularios:
            for chave in item:
                if chave in chaves_desejadas:
                    valores_encontrados[chave] = item[chave]
                    chaves_desejadas.remove(chave)  # Remover a chave já encontrada
                    if not chaves_desejadas:  # Se todas as chaves foram encontradas, sair do loop
                        break

        # Atribuir os valores a variáveis individuais (opcional)
        dtajuizamento = valores_encontrados.get('dtajuizamento')
        dtcitacao = valores_encontrados.get('dtcitacao')
        dtatualizacao = valores_encontrados.get('dtatualizacao')
        dtiniciocalculo = valores_encontrados.get('dtiniciocalculo')
        termofinalC = valores_encontrados.get('termofinalC')
        termofinalF = valores_encontrados.get('termofinalF')
        termofinalR = valores_encontrados.get('termofinalR')
        pagamento = valores_encontrados.get('pagamento')
        anoinipagto = valores_encontrados.get('anoinipagto')
        anofimpagto = valores_encontrados.get('anofimpagto')
        tabpnep = valores_encontrados.get('tabpnep')
        tabjuros = valores_encontrados.get('tabjuros')
        verificarObito = valores_encontrados.get('verificarObito')        
        aplicarSELIC = valores_encontrados.get('aplicarSELIC')
        aplicarSELIC = {'on': True, 'off': False}.get(aplicarSELIC, None)
        selicJuros = valores_encontrados.get('selicJuros')
        selicJuros = {'on': True, 'off': False}.get(selicJuros, None)

        lista_tabelas = ApiIndice.get_cod_nome_desc_das_tabelas()
        tabela_pnep = Utils.obter_codigo_por_descricao(lista_tabelas, tabpnep)
        tabela_juros = Utils.obter_codigo_por_descricao(lista_tabelas, tabjuros)

        
        # montar um dicionário de dataframes para cada cpf de exequente
        prefixo_2886_df = TabelasSerpro.tabela_2886_sicape(simplificado, completo, dict_formularios)
        #info(f"{DateTools.converter_ano_mes_dia_para_string(dtcitacao)}\n{DateTools.converter_ano_mes_dia_para_string(dtatualizacao)}\n{DateTools.converter_ano_mes_dia_para_string(dtiniciocalculo)}\n{DateTools.converter_ano_mes_dia_para_string(termofinalC)}\n")

    
        # sufixo_2886_df = cls.montar_sufixo(tabela_juros, 
        #                                    tabela_pnep, 
        #                                    DateTools.converter_ano_mes_dia_para_string(dtcitacao), 
        #                                    DateTools.converter_ano_mes_dia_para_string(dtatualizacao), 
        #                                    DateTools.converter_ano_mes_dia_para_string(dtiniciocalculo), 
        #                                    DateTools.converter_ano_mes_dia_para_string(termofinalC), 
        #                                    aplicarSELIC, 
        #                                    selicJuros)

        tabela = Tabelas(tabela_juros, 
                         tabela_pnep,
                         DateTools.converter_ano_mes_dia_para_string(dtcitacao),
                         DateTools.converter_ano_mes_dia_para_string(dtatualizacao), 
                         DateTools.converter_ano_mes_dia_para_string(dtiniciocalculo),
                         DateTools.converter_ano_mes_dia_para_string(termofinalC),
                         aplicarSELIC,
                         selicJuros
                        )

        sufixo_2886_df = tabela.sufixo()
 
                
        info(f"------------- PREFIXO ---------------\n{prefixo_2886_df}")

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option("display.float_format", "{:.4f}".format)

        info(f"------------- SUFIXO ----------------\n{sufixo_2886_df}")
        
        
        #sufixo_2886_df = cls.montar_sufixo()
        
        # sufixo = 
        # buscar Iam, juros, selic
        # aplicar teto
        # aplicar percentuais
        # aplicar pro-rata
        # aplicar segundo percentual.

        # pd.set_option('display.max_rows', None)
        # pd.set_option('display.max_columns', None)
        # pd.set_option("display.float_format", "{:.2f}".format)



        # # Exibir o resultado
        # for exequente in prefixo_2886_df:
        #     info(f"Exequente: {exequente['nome']} (CPF: {exequente['cpf']})")
        #     info("DataFrames:")
        #     for idx, categoria in enumerate(['C', 'F', 'R', 'P']):
        #         info(f"DataFrame {categoria}:")
        #         info(f"\n{exequente['dataframes'][idx]}\n")
        #     info("\n")

    

        return prefixo_2886_df   
    

        """
            a data_inicio_cálculo pode não começar no dia primeiro do mês, situação que deverá ser aplicado o pró-rata.
            Assim, a data_inicio_periodo será a data_inicio_calculo só que no dia primeiro.        
            tabela_pnep = 't302_juros'
        """  
    # @classmethod
    # def _montar_sufixo(cls, 
    #                   tabela_juros: str, 
    #                   tabela_pnep: str, 
    #                   dt_citacao: str, 
    #                   dt_atualizacao: str, 
    #                   dt_inicio_calculo: str, 
    #                   dt_final_calculo: str, 
    #                   aplicar_selic: bool, 
    #                   aplicar_selic_juros: bool) -> pd.DataFrame:
        
  
    #     if aplicar_selic:
    #         juros = MatrizIndices.matriz_tabela_juros(tabela_juros, dt_citacao, dt_atualizacao)
    #         indice = MatrizIndices.matriz_tabela_pnep(tabela_pnep)
    #         selic = MatrizIndices.matriz_selic_acumulada(dt_inicio_calculo, dt_atualizacao)
    #         parte1 = pd.merge(indice, juros, on='data', how='inner')
    #         sufixo = pd.merge(parte1, selic, on='data', how='inner')
            
    #         pd.set_option('display.max_rows', None)
    #         pd.set_option("display.float_format", "{:.8f}".format)
            
    #         info(f"SUFIXO:\n{sufixo}")
        
    #     return sufixo
    
    
    
