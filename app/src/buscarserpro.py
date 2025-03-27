
from api_utils import *

from configura_debug import *

from acd_api_serpro import *

from acd_api_serpro import *
from acd_serpro_calculo import *
import pandas as pd


# Rubricas utilizadas no cálculo - retirar a 00176 - Gratificação Natalina.
rubricasCalculo = [
    1, 5, 13, 18, 24, 25, 34, 53, 58, 65,
    73, 79, 92, 117, 130, 136, 192, 173, 174, 175,
    197, 220, 330, 561, 593, 621, 665, 678, 679, 700,
    740, 743, 826, 852, 973, 974, 982, 1033, 1738, 1761,
    1762, 8798, 10289, 16135, 19196, 30214, 30324, 30657, 30658, 30694,
    31000, 31492, 71157, 71162, 72507, 72554, 72556, 72746, 73359, 73460,
    73580, 98002, 98004, 98012, 98027, 98502, 99001, 99003, 99004
]

rubricasCalculo = [
    1, 13, 65, 192, 220, 852 
]


rubricasAT = [507, 513]  # Rubricas abate-teto
rubricasPagtosAdm = [19196,82174, 82175, 82176]  # Rubricas pagamento administrativo

orgao = ''

dataInicio = "21/07/1995" # termo inicial
dataFinal = "01/07/1999"  # termo final

dataInicioPagtoAdm = "01/12/2002"
dataFinalPagtoAdm = "01/08/2009"

# data citacao
# data atualizacao

dataFinal = dataFinalPagtoAdm # a data final da extração deve ser a data final dos pagtos adms.

orgao = None
#cpf = '48809144104'

# pensionista IVANI TEREZINHA POSSAN#
cpf = '36030007068'
anoi = '2019'
anof = '2024'
anof = '2020'

# instituidor CARLOS GUILHERME POSSAN
cpf = '13197240006'

cpf, anoi, anof ='19459696449', '1995','2004'
#cpf, anoi, anof = '48809144104', '2002', '2025' # orgao 41231


cpf = '24733830904' # luis carlos de assuncao


termoInicial = '21/07/1995'
termoFinal = '31/12/2001'
dataCitacao = '01/09/1995'
dataAtualizacao = '30/06/2022'
anoInicio = 1995
anoFinal = 2004
percentual = 100
orgao = None



df1, df2, rubricas_cabecalho = TabelasSerpro.tabelaTrezDezessete(cpf, 
                                             anoInicio, 
                                             anoFinal, 
                                             rubricasCalculo,
                                             rubricasPagtosAdm, 
                                             termoInicial,
                                             termoFinal,
                                             dataCitacao,
                                             dataAtualizacao,
                                             percentual,
                                             orgao)


# Exibir o DataFrame final
pd.set_option('display.max_rows', None)
#pd.set_option('display.max_columns', None)
pd.set_option("display.float_format", "{:.4f}".format)

# #info(f'\n{df_final}')
print(f'df_calculo:\n{df1}')
print(f'df_pagtos:\n{df2}')
print(f'\n{rubricas_cabecalho}\n')      
#info(f'\n{rendimentos}\n')




'''
(cls, 
                            cpf: str, 
                            anoi: int, 
                            anof: int, 
                            basecalculo: list, 
                            basepgtos: list,
                            termo_inicial: str,
                            termo_final: str,
                            data_citacao: str,
                            data_atualizacao: str,
                            percentual: int, 
                            orgao: Optional[int] = None):
      
'''


# for i in dados:
#     print(f'lista:\n{i}')      

#dados2 = SerproSiape.extrair_ficha_financeira(cpf, anoi, anof)
#dados2 = SerproSiape.consultar_beneficiario(cpf)
#dados2 = SerproSiape.consultar_beneficiario_instituidores(cpf)

#dados2 = SerproSiape.pesquisar_beneficiario_pelo_nome('CELINA MARIA')
#dados2 = SerproSiape.pesquisar_servidor_cpf_request(cpf)
#print(dados2)


'''
# Listar os métodos disponíveis
print("Métodos disponíveis no serviço SOAP:")
print(dir(client.service))
'''



'''

print(client.service)

for service in client.wsdl.services.values():
    for port in service.ports.values():
        operations = port.binding._operations
        for name, operation in operations.items():
            print(f"Método: {name}")
            print(f"  Entrada: {operation.input.signature()}")
            print(f"  Saída: {operation.output.signature()}")
            print("-" * 40)

'''            
'''
methods = [op for op in client.service.__dir__() if not op.startswith("_")]
print(methods)

'''


#print(dados2)

       

# Exibir resultado
#pd.set_option('display.max_rows', None)
#pd.set_option("display.float_format", "{:.8f}".format)
#df = pd.DataFrame(dados_brutos)
#print(df)
