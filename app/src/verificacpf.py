""" 
Esta função recebe uma string com os cpfs para processar
e retorna um dicionário contendo duas listas, a lista de 
cpfs válidos e a lista de cpfs inválidos:

listacpf = {'validos': [], 'invalidos': []}

a função também retira a formatação e preenche os zeros 
à esquerda que estiverem faltando
"""

import re
import random

global CPF_LENGHT
global BLACKLIST

CPF_LENGHT = 11
BLACKLIST = [
  '00000000000',
  '11111111111',
  '22222222222',
  '33333333333',
  '44444444444',
  '55555555555',
  '66666666666',
  '77777777777',
  '88888888888',
  '99999999999',
];

def __numberToWeightArray(weight, length):
    array = []
    for i in range(length):
        array.append(weight - i)
    return array

def __createChecksum(base, weights):
    aggregator = 0
    for index, digit in enumerate(base):
        aggregator += int(digit) * weights[index]    
    return aggregator

def __generateChecksum(base, weights):
    numericBase = re.sub("[^0-9]", "", str(base))
    if isinstance(weights, int):
        weightsArray = __numberToWeightArray(weights, len(numericBase))
        return __createChecksum(numericBase, weightsArray)
    elif isinstance(weights, list):
        return __createChecksum(numericBase, weights)
    else:
        raise Exception('Invalid weight type. Should be an Array like or a Number')

def formater(cpf):
    cpf = str(cpf)
    return '{0}.{1}.{2}-{3}'.format(cpf[0:3], cpf[3:6], cpf[6:9], cpf[9:11])

def validate(cpf):
    # Remove char não numéricos
    stringCpf = re.sub("[^0-9]", "", str(cpf))
    
    if (len(stringCpf) < CPF_LENGHT) or (len(stringCpf) > CPF_LENGHT):
        return False
    elif stringCpf in BLACKLIST:
        return False
    else:
        cpfRoot = stringCpf[:(CPF_LENGHT-2)]
        check1 = stringCpf[-2]
        check2 = stringCpf[-1]

        expectedCheck1 = __generateChecksum(cpfRoot, 10) % 11
        if expectedCheck1 < 2:
            expectedCheck1 = 0
        else:
            expectedCheck1 = 11 - expectedCheck1
        expectedCheck2 = __generateChecksum(cpfRoot + str(expectedCheck1), 11) % 11
        if expectedCheck2 < 2:
            expectedCheck2 = 0
        else:
            expectedCheck2 = 11 - expectedCheck2

        if (int(check1) == expectedCheck1) and (int(check2) == expectedCheck2):
            return True
        else:
            return False


def validarCPF(cpf_str):
    listacpf = {'validos': [], 'invalidos': []}
    cpf_split = cpf_str.replace('-', '').replace('.', '').split()
    for cpf in cpf_split:
        cpf = cpf.zfill(11)  # Preenche com zeros à esquerda se o CPF for menor que 11 dígitos
        valido = validate(cpf)
        if valido:
            listacpf['validos'].append(cpf)
        else:
            listacpf['invalidos'].append(cpf)
    return listacpf



# def validarCPF(cpf_str):
    
#     lista = []
#     valido = False
#     listacpf = {'validos':[],'invalidos':[]}
    
#     cpf_split = cpf_str.split()
    
#     for cpf in cpf_split:
#         cpf = cpf.replace('-','')
#         cpf = cpf.replace('.','')
#         tam = len(cpf)
#         if tam<11:
#             zeros = "0"* (11 - tam)
#             cpf = zeros + cpf
        
#         valido = validate(cpf)
#         if valido:
#             listacpf['validos'].append(cpf)
#         else:
#             listacpf['invalidos'].append(cpf)       
    
#     return listacpf
