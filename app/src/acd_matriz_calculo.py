from src.acd_indices_calculo import Tabelas


class MatrizCalculo:
    ...

    # def matriz_iam_juros(cls,
    #                     tabela_juros: str,
    #                     tabela_pnep: str,
    #                     data_citacao: str,
    #                     data_atualizacao: str,
    #                     data_inicio_periodo: str,
    #                     data_final_periodo: str,
    #                     aplicar_selic: bool,
    #                     aplicar_selic_juros: bool):
            
            
    #         juros = Tabelas.juros('t302_juros',   # tabela
    #                                             '01/09/1995',   # data_citacao
    #                                             '01/12/2021',   # data_atualizacao
    #                                             '01/07/1995',   # data_inicio_periodo
    #                                                 '30/06/2022',   # data_final_periodo
    #                                                 True,           # aplicar_selic   
    #                                                 True)           # aplicar_selic_sobre_juros
        
    #         indice = Tabelas.indice('t200_tabela_pnep',   # nome_tabela
    #                                                 '01/07/1995',         # data_inicial       
    #                                                 '30/06/2022',         # data_final
    #                                                 '01/12/2021'          # data_atualizacao
    #                                                 )
        

    #         selic = Tabelas.selic('',             # data_citacao
    #                                                 '30/06/2022',   # data_atualizacao
    #                                                 '21/07/1995',   # data_inicio_calculo
    #                                                 '30/06/2022',   # data_final_periodo
    #                                                 True,           # aplicar_selic
    #                                                 True            # aplicar_selic_sobre_juros
    #                                                 )
                                
    #         parte1 = pd.merge(indice, juros, on='data', how='inner')
    #         sufixo = pd.merge(parte1, selic, on='data', how='inner')
    #         return (sufixo)