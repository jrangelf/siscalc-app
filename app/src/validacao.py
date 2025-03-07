""" 
Verifica se o cpf é válido, retornando uma lista com os cpfs inválidos 

"""

from src.verificacpf import validarCPF, formater



def verifica_campos_entrada(numero_cpf, nome_arquivo, varios_cpf, lista_de_erros):
	
	#print("#---------------validacao.py----------------------")
	#print("# (verifica_campos_entrada)-> nome_arquivo: ", nome_arquivo)
	#print("#-------------------------------------------------")
	
	if numero_cpf == '' and nome_arquivo == '' and varios_cpf == '':
			lista_de_erros ['numero_cpf'] = 'Deve-se escolher pelo menos um tipo de busca: Individual, Lista ou por leitura de Arquivo'
		
	if numero_cpf == None and nome_arquivo == None and varios_cpf == None:
			lista_de_erros ['numero_cpf'] = 'Deve-se escolher pelo menos um tipo de busca: Individual, Lista ou por leitura de Arquivo'
	

	if numero_cpf != '' and nome_arquivo != '' and varios_cpf != '':
			lista_de_erros ['numero_cpf'] = 'Apenas um tipo de busca deve ser utilizado: Individual, Lista ou por Arquivo'
		


def verifica_validade_cpf(numero_cpf, nome_do_campo, lista_de_erros, modulo):	
	# passa uma string (numero_cpf) com os números de CPF separados por espaço e
	# recebe como retorno um dicionário lista_cpf =  {'validos':[],'invalidos':[]}
	
	lista_invalidos = []
	listacpf = validarCPF(numero_cpf)
	lista_invalidos = listacpf['invalidos']


	
	if len(lista_invalidos) != 0:
		
		#grava_arquivo_cpfs_invalidos(lista_invalidos,modulo)		
		
		if len(lista_invalidos) > 1:
			prefixo = "CPFs inválidos: "
		else:
			prefixo = "CPF inválido: "

		invalidos_formatados=[]
		invalidos_formatados.append(prefixo)

		for invalido in lista_invalidos:
			invalido = formater(invalido)
			invalidos_formatados.append(invalido) 
			
		texto =  invalidos_formatados
		lista_de_erros[nome_do_campo] = texto

		#print("#--------------validacao.py-----------------------")
		#print("# lista_inválidos: ", lista_invalidos)
		#print("#-------------------------------------------------")
		#print("# lista_inválidos_formatados: ", invalidos_formatados)
		#print("#-------------------------------------------------")
		
	
	return listacpf



def verifica_nome_arquivo(nome_arquivo,nome_do_campo,lista_de_erros):
	#print("#---------------validacao.py----------------------")
	#print('# Nome do arquivo: ',nome_arquivo)
	#print("#-------------------------------------------------")
	pass


def verifica_validade_cpf_arquivo(lista_numero_cpf,nome_do_campo,lista_de_erros):
	pass



