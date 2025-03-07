from acd_api_indices import *

# Exibir o DataFrame final
pd.set_option('display.max_rows', None)
pd.set_option("display.float_format", "{:.8f}".format)

juros = TabelasApi.obterTabelaJuros('t302_juros',   # tabela
                                            '01/09/1995',   # data_citacao
                                            '01/12/2021',   # data_atualizacao
                                            '01/07/1995',   # data_inicio_periodo
                                            '30/06/2022',   # data_final_periodo
                                            True,           # aplicar_selic   
                                            True)           # aplicar_selic_sobre_juros
#print(f'juros:\n{juros}')


# tabela, data_inicial, data_final, data_atualizacao
indice = TabelasApi.obterTabelaIndice('t200_tabela_pnep',   # nome_tabela
                                              '01/07/1995',         # data_inicial       
                                              '30/06/2022',         # data_final
                                              '01/12/2021'          # data_atualizacao
                                             )
#print(f'indice:\n{indice}')


selic = TabelasApi.obterTabelaSelic('',             # data_citacao
                                            '30/06/2022',   # data_atualizacao
                                            '21/07/1995',   # data_inicio_calculo
                                            '30/06/2022',   # data_final_periodo
                                            True,           # aplicar_selic
                                            True            # aplicar_selic_sobre_juros
                                            )
                        
#print(f'selic\n{selic}')

parte1 = pd.merge(indice, juros, on='data', how='inner')
sufixo = pd.merge(parte1, selic, on='data', how='inner')
print(sufixo)





