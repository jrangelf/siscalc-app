from re import S
from .forms import ObitoForm, RubricasForm, ListForm, UploadFileForm, List
from datetime import datetime

from io import TextIOWrapper

from django.shortcuts import render, redirect 
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from src.verificacpf import validarCPF, formater
from src.acd_tabelas import montar_tabela

from src.api_serpro import *
from src.api_indice import *
from src.acd_utils import Utils
from src.acd_main import *
from src.acd_serpro_calculo import *
from src.acd_calculos import * 

from .models import *
from src.acd_indices_calculo import Tabelas

from src.acd_html_paser import *
from src.acd_gera_pdf import *
from src.acd_gera_pdf_old import *
from src.acd_gera_excel import *

from src.configura_debug import *
from src.acd_datetools import DateTools

import pandas as pd

def ficha(request):
	return render(request,'ficha.html',{})

def fichalista(request):	
	listacpf = {}
	lista_validos = []
	if request.method == "POST":
		cpf = request.POST.get('cpf')
		anoi = request.POST.get('anoinicial')
		anof = request.POST.get('anofinal')				
		listacpf = validarCPF(cpf)  
		lista_validos = listacpf['validos']
		lista_invalidos = listacpf['invalidos']
		total_invalidos = len(lista_invalidos)		
		if total_invalidos > 0:
			messages.success(request, (f"CPF {cpf} inválido."))			
		fichas = obter_ficha_financeira(lista_validos, anoi, anof)				
	return render(request,'ficha-lista.html',{'fichas':fichas})

def rubricas(request):
	form = RubricasForm() 
	contexto = {'form': form}	
	return render(request,'rubricas.html',contexto)

def rubricaslista(request):
	if request.method == "POST":		
		form = RubricasForm(request.POST)
		anoinicial = request.POST.get('anoinicial')
		anofinal = request.POST.get('anofinal')
		orgao = request.POST.get('orgao')
		#info(f"extratorlista:orgao: {orgao}")
		itens = list(dict(request.POST.items()).values())
		rubricas = itens[4:14]
		lista_cpfs = itens[14]
		listacpf = validarCPF(lista_cpfs) 
		lista_validos = listacpf['validos']				
		lista_invalidos = listacpf ['invalidos']
		total_invalidos = len(lista_invalidos)		
		msg = '\n'.join(lista_invalidos)
		if total_invalidos > 1:
			msg = f"CPFs inválidos: {msg}"			
		elif total_invalidos == 1:
			msg = f"CPF inválido: {msg}"
		if total_invalidos != 0:
			messages.success(request, (msg))
		contexto, desc_rubricas = extrair_rubricas(lista_validos, anoinicial, anofinal, orgao, rubricas)		
	return render(request,'rubricas-lista.html',{'livro':contexto,
												'rubricas':desc_rubricas,
												'ano':[anoinicial, anofinal],
												'validos':lista_validos})

def obitos(request):	
	form = ObitoForm()
	contexto = {'form': form}	
	return render(request,'obitos.html',contexto)

def obitoslista(request):	
	if request.method == "POST":		
		form = ObitoForm(request.POST, request.FILES)
		unico = request.POST.get('numero_cpf')
		varios = request.POST.get('varios_cpf')			
		# vefica qual campo tem mais cpfs 
		if len(unico) > len(varios):
			listacpf = validarCPF(unico)
		else:
			listacpf = validarCPF(varios)
		lista_validos = listacpf['validos']		
		lista_invalidos = listacpf ['invalidos']
		total_invalidos = len(lista_invalidos)
		num_invalidos = str(total_invalidos)
		msg = '\n'.join(lista_invalidos)
		if unico=='' and varios == '':
			messages.success (request, ('Você deve inserir pelo menos um CPF para pesquisar'))
		if total_invalidos > 1:
			msg = num_invalidos + ' CPFs inválidos: '	+ msg
		else:
			if total_invalidos == 1:
				msg = num_invalidos + ' CPF inválido: ' + msg
		if total_invalidos != 0:
			messages.success(request, (msg))
		items = obter_data_obito(lista_validos)				
		return render(request,'obitos-lista.html',{'items':items})
	else:
		form = ObitoForm()
		contexto = {'form': form}		
		return render(request, 'obitos-lista.html',contexto)

def tabelaspnep(request):
	tipo = request.GET.get('type', None)	
	#lista_tabelas = APIData.listar_tabelas()
	lista_tabelas = ApiIndice.get_lista_completa_das_tabelas()
	
	'''
	lista_tabelas = [
	[100, 'Tabela INPC', 'inpc', 'Índice nacional de preços ao consumidor'],	
	[200, 'Tabela c.m. cond. geral IPCA-E', 't200_tabela_pnep', ...],
	[220, 'TR FEV/91 em diante', 't220_tabela_pnep', None], 
	[222, 'Tabela c.m. benef. INPC', 't222_tabela_pnep', 'OBS: Se o valor original...]
	]	  
	'''
		
	if request.method == 'POST':
		return render(request,'tabelas.html', {})		
	else:
		if tipo == 'bcb':
			lista = [item[1] for item in lista_tabelas if item[0] < 200]
		elif tipo == 'pnep':
			lista = [item[1] for item in lista_tabelas if 200 <= item[0] < 300]
		elif tipo == 'juros':
			lista = [item[1] for item in lista_tabelas if 300 <= item[0] < 400]
		else:
			lista = [4]
		return render(request,'tabelas.html', {'tabelas':lista, 'tipo': tipo})

def tabelaspnep_lista(request):	
	if request.method == 'POST':		
		lista_tabelas = ApiIndice.get_lista_completa_das_tabelas()
		titulo_da_tabela = list(dict(request.POST.items()).values())[1]
		tupla_nome_obs_cod = [(item[2],item[3], item[0]) for item in lista_tabelas if item[1] == titulo_da_tabela]		
		nome_tabela, observacao, codigo = tupla_nome_obs_cod[0][0], tupla_nome_obs_cod[0][1], tupla_nome_obs_cod[0][2]
		dados = ApiIndice.get_tabela(nome_tabela)
		contexto = montar_tabela(titulo_da_tabela, observacao, dados, codigo)
		
		#info(f'|titulo_da_tabela|\n{titulo_da_tabela}')
		#info(f'|tupla_nome_obs_cod|\n{tupla_nome_obs_cod}')
		#info(f'|nome_tabela|\n{nome_tabela}')
		#info(f'|observacao|\n{observacao}')
		#info(f'|nome_tabela|\n{codigo}')
		#info(f'|dados|\n{dados}')
		#info(f"|contexto|\n {contexto}")
					
		return render(request, 'tabelas-lista.html', {'tabelas': lista, 'contexto': contexto})
	return render(request, 'tabelas-lista.html',{})

def resumo(request):
	x=0
	if request.method == 'POST':
		print('via post')
		x = 1
		return render(request, 'resumo.html',{})
	else:
		print('via get')
		return render(request, 'resumo.html', {'x':x})	

 	

#----------------------------------------------------------------------------------------------------------------------
#####   #####      #####    #####
    #  #     #    #     #  #
    #  #     #    #     #  #
#####   #####      #####   #####
#      #     #    #     #  #    #
#      #     #    #     #  #    #
#####   #####  #   #####   ##### 
#----------------------------------------------------------------------------------------------------------------------

def calculo2886(request):

	if request.method == "POST":
			
		# cria um dicionário com todos os itens dos formulários
		dict_formularios = [{key: value} for key, value in request.POST.items()]
		del dict_formularios[0]
		
		arquivo_simplificado = TextIOWrapper(request.FILES['arquivo_simplificado'].file, encoding='latin-1')
		arquivo_completo = TextIOWrapper(request.FILES['arquivo_completo'].file, encoding='latin-1')

		#info(f"DICT_FORMULARIOS:\n{dict_formularios}")
		#campos, rubricas_base_2886 = Utils.extrair_campos(dict_formularios)
		
		df_calculo2886 = Calculos.calcular_2886_sicape(arquivo_simplificado, arquivo_completo, dict_formularios)

		info(f"DF-CALCULO2886 (DATAFRAME) ********************************\n{df_calculo2886}")

		# Converte os dataframes para dicionários (serializáveis)
		for item in df_calculo2886:
			if 'dataframes' in item and isinstance(item['dataframes'], tuple):
				item['dataframes'] = tuple(
                    df.to_dict(orient='records') if not df.empty else {}  # Converte para dicionário ou vazio
                    for df in item['dataframes']
                )
		
		#info(f"DF-CALCULO2886 (DICIONÁRIO) ********************************\n{df_calculo2886}")

		
		"""
		aqui views vai chamar o método Calculos.calcular2886_sicape(resultado, arquivo_simplificado, arquivo_completo)
		na Classe Calculos, há um método chamado calcular2886_sicape.

		esse método chama, TabelaSerpro.tabela2886_sicape(resultado, arquivo_simplificado, arquivo_completo) para montar o 
		dataframe dos valores de rendimentos do 2886. 
		em seguida, calcular2886_sicape, vai buscar os IAM, Juros e Selic em X.

		com os dataframes dos indices e os dataframes dos rendimentos, vai montar a tabela de cálculo, fazendo 
		um merge dos dois.

		deve retorna um dataframe para os calculos e um dataframe para o consolidado.
		
		"""


		# # cria um dicionário para os campos e uma lista de dicionários para as rubricas retirando as de tipo 'N'
		campos, rubricas_base_2886 = Utils.extrair_campos(dict_formularios)
		# #info(f'CAMPOS:\n{campos}')
		# #info(f'rubricas_base_2886:\n{rubricas_base_2886}')
		
		# Armazenar os dados na sessão
		request.session['campos'] = campos
		request.session['df_calculo2886'] = df_calculo2886
		#request.session['varios_cpf_pensionista'] = varios_cpf_pensionista
		request.session['rubricas'] = rubricas_base_2886		
		
		return redirect('resultado2886')
	
	
	else:		
		lista_tabelas = ApiIndice.get_lista_completa_das_tabelas()		
		teste = [[item[0], item[1], item[2]] for item in lista_tabelas if 200 <= item[0] < 400]
		lista_tabelas_indices = [item[1] for item in lista_tabelas if 200 <= item[0] < 300]
		lista_tabelas_juros = [item[1] for item in lista_tabelas if 300 < item[0] < 312]

		#info(f'pnep:\n{lista_tabelas_indices}\njuros:\n{lista_tabelas_juros}')
		
		#queryset = TbBase317.objects.filter(tipo='S').values('codigorubrica', 'nomerubrica', 'tipo')
		#queryset = TbBase2886.objects.values('codigorubrica', 'nomerubrica', 'tipo')
		queryset = TbBase2886.objects.values('codigorubrica', 'nomerubrica', 'tipo').order_by('codigorubrica')
		#info(f'queryset:\n{queryset}')
		return render(request,'calculo2886.html',{
			'pnep':lista_tabelas_indices, 
			'juros': lista_tabelas_juros,
			'items':queryset,			
			'teste':teste})



def resultado2886(request):
		
		calculo = request.session.get('df_calculo2886')
		
		if calculo is None:
			info("Nenhum dado encontrado na sessão.")
			return render(request, 'resultado2886.html', {'resultado': ''})


		# processar e ajustar os dados antes de renderizar o template, formatar a data e os números
		for item in calculo:
			if 'dataframes' in item:
				dataframes_processados = []
				for df in item['dataframes']:
					if df:						
						for row in df:
							for key, value in row.items():
								
								if isinstance(value, (int, float)):  # Verifica se é número (int ou float)
									#row[key] = f"{value:.2f}".replace('.', ',')  # Formata para duas casas decimais e ponto para o milhar
									#row[key] = f"{value:,.2f}".replace('.', ',').replace(',', '.', 1)  # Troca a vírgula para ponto e coloca espaço no milhar
									row[key] = f"{value:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')

								# Converter datas para formato "03/1993"
								if key.lower() == 'mês/ano' and isinstance(value, str): # verifica se a data é (str)									
									try:										
										value = datetime.strptime(value, '%Y-%m-%d').strftime('%m/%Y')
										row[key] = value
									except ValueError:
										pass
								# formatar para 2 casas decimais os números
								#elif isinstance(value, (int, float)):
								#	row[key] = round(value, 2)
						dataframes_processados.append(df)
					else:
						dataframes_processados.append([])
				item['dataframes'] = dataframes_processados
		
		
		# Renderizar o template com os dados
		return render(request, 'resultado2886.html', {'resultado': calculo})



# def resultado2886(request):
# # Recuperar os dados da sessão
# 	#resultado = request.session.get('df_calculo2886', 'Nenhum resultado disponível.')
# 	campos = request.session.get('campos', 'Nenhuma rubrica disponivel')
# 	lista_ativo = []
# 	lista_pensionista = []
# 	#resultado = request.session.get('dicionario_df', '')
# 	#info(f"resultado:\n{resultado}")

# 	resultado = [
#         {
#             'iu': 8922020,
#             'cpf': '134.927.136-53',
#             'nome': 'VERA LUCIA DUARTE',
#             'matricula': '0',
#             'beneficiario': '0',
#             'cargo': '11-3/AIII',
#             'dataframes': (
#                 pd.DataFrame({
#                     "Mês/Ano": ["1993-01-01", "1993-02-01", "1993-03-01"],
#                     "1": [6545668.00, 9737260.00, 11471171.32],
#                     "5": [0.0, 0.0, 0.0],
#                     "13": [130913.36, 707585.94, 445986.36]
#                 }),
#                 pd.DataFrame({
#                     "Mês/Ano": ["1993-01-01", "1993-02-01", "1993-03-01"],
#                     "15": [1680143.50, 1680143.50, 2234590.85],
#                     "24": [0.00, 110515.81, 0.00],
#                     "25": [1320112.75, 1320112.75, 1755749.95]
#                 }),
#                 pd.DataFrame(),  # DataFrame vazio
#                 pd.DataFrame({
#                     "Mês/Ano": ["2002-12-01", "2003-08-01", "2003-12-01"],
#                     "82175": [366.37, 393.59, 956.66]
#                 })
#             )
#         }
#     	]

	
# 	for item in resultado:
# 		if 'dataframes' in item and isinstance(item['dataframes'], tuple):
# 			item['dataframes'] = tuple(
#                 df.to_html(index=False, classes='table table-striped') if not df.empty else '<p>Nenhum dado disponível</p>'
#                 for df in item['dataframes']
#             )
	
# 	return render(request, 'resultado2886.html', {'resultado': resultado, 'campos': campos})# for item in resultado:

#----------------------------------------------------------------------------------------------------------------------	

			####     ##   ######  
			   ##   ###       ##  
			   ##    ##      ##  
			####     ##     ##  
			   ##    ##    ##  
			   ##    ##   ##   
			####  #  ##  ##  

#----------------------------------------------------------------------------------------------------------------------
def calculo317(request):
	if request.method == "POST":
		
		# cria um dicionário com os itens dos formulários
		itens_formulario_dict = [{key: value} for key, value in request.POST.items()]
		del itens_formulario_dict[0] # apaga o token
		
		varios_cpf_ativo = request.POST.get('varios_cpf_ativo', '')
		varios_cpf_pensionista = request.POST.get('varios_cpf_pensionista', '')
		
		df_calculo317 = Calculos.calcular_317(itens_formulario_dict, varios_cpf_ativo, varios_cpf_pensionista)

		
		
		
		# Exibir os resultados
		#info(f"calculo317:Ativos/Aposentados:\n{varios_cpf_ativo}")
		#info(f"calculo317:Pensionistas:\n{varios_cpf_pensionista}")		

		#df_calculo317 = Calculos.calcular_317(dict_campos, varios_cpf_ativo, varios_cpf_pensionista)
		#info(f"dicionario de campos:\n{itens_formulario_dict}")

		
		
		# Criar um dicionário para agrupar os códigos, descrições e tipos
		dados = {}
		for d in itens_formulario_dict:
			for k, v in d.items():
				dados[k] = v

		#info(f"dados:\n{dados}")

		## Identificar as chaves a serem removidas
		chaves_para_remover = set()
		for key, value in dados.items():
			if key.startswith("tipo_") and value == "N":
				codigo_key = f"codigo_{key.split('_')[1]}"
				descricao_key = f"descricao_{key.split('_')[1]}"
        		# Adicionar as chaves para remoção
				chaves_para_remover.update([codigo_key, descricao_key, key])

		#info(f"chaves para remover:\n{chaves_para_remover}")
		
		# Remover as chaves identificadas
		for key in chaves_para_remover:
			dados.pop(key, None)

		# Criar uma nova lista de dicionários com os dados filtrados
		rubricas = [{k: v} for k, v in dados.items() if k.startswith("codigo_") or k.startswith("descricao_") or k.startswith("tipo_")]
		#info(f"rubricas:\n{rubricas}")

		# Armazenar os dados na sessão
		request.session['campos'] = itens_formulario_dict
		request.session['varios_cpf_ativo'] = varios_cpf_ativo
		request.session['varios_cpf_pensionista'] = varios_cpf_pensionista
		request.session['rubricas'] = rubricas		
		
		return redirect('resultado317')
	
	
	else:

		form = ObitoForm()
		lista_tabelas = ApiIndice.get_lista_completa_das_tabelas()
		
		teste = [[item[0], item[1], item[2]] for item in lista_tabelas if 200 <= item[0] < 400]
		#info(f'teste:\n{teste}')

		lista_tabelas_indices = [item[1] for item in lista_tabelas if 200 <= item[0] < 300]
		lista_tabelas_juros = [item[1] for item in lista_tabelas if 300 < item[0] < 312]

		#info(f'pnep:\n{lista_tabelas_indices}\njuros:\n{lista_tabelas_juros}')
		
		#queryset = TbBase317.objects.filter(tipo='S').values('codigorubrica', 'nomerubrica', 'tipo')
		queryset = TbBase317.objects.values('codigorubrica', 'nomerubrica', 'tipo')
		#info(f'queryset:\n{queryset}')
		return render(request,'calculo317.html',{
			'pnep':lista_tabelas_indices, 
			'juros': lista_tabelas_juros,
			'items':queryset,
			'form':form,
			'teste':teste})




def resultado317(request):
	# Recuperar os dados da sessão
	resultado = request.session.get('campos', 'Nenhum resultado disponível.')
	lista_ativo = []
	lista_pensionista = []

	for item in resultado:
		for key, value in item.items():
			if key == "varios_cpf_ativo":
				lista_ativo = value.splitlines()  # Quebra em lista, removendo linhas vazias
			elif key == "varios_cpf_pensionista":
				lista_pensionista = value.splitlines()

	# Limpar espaços extras e remover linhas vazias
	lista_ativo = [cpf.strip() for cpf in lista_ativo if cpf.strip()]
	lista_pensionista = [cpf.strip() for cpf in lista_pensionista if cpf.strip()]

	# Exibir os resultados
	info("Ativos/Aposentados:", lista_ativo)
	info("Pensionistas:", lista_pensionista)


	#cpf_ativos = request.session.get('varios_cpf_ativo', '')
	#cpf_pensionistas = request.session.get('varios_cpf_pensionista')
	#info(f'ativos:\n{cpf_ativos}')
	#info(f'pensionistas:\n{cpf_pensionistas}')
	
	return render(request, 'resultado317.html', {'resultado': resultado})


# ['zr7mO0gJwdohzTBmZBp8y9CRC2AZwybVvYLeDbeSNIldgZvy0i3wa95ToOKLSjon', '2025-03-06', 
# '2025-03-07', '2025-03-08', '2025-03-10', '2025-03-11', 'Tabela c.m. cond. geral IPCA-E', 
# 'Juros 0,5% até junho de 2009', 'on']










def indices(request):
	if request.method == 'POST':
		valores = list(dict(request.POST.items()).values())		
		_, dt_citacao, dt_atualiza, dt_inicio, dt_final, iam, juros, selic = valores 
		
		#data_ajuizamento = DateTools.converter_ano_mes_dia_para_string(dt_ajuizamento)
		data_citacao = DateTools.converter_ano_mes_dia_para_string(dt_citacao)
		data_atualizacao = DateTools.converter_ano_mes_dia_para_string(dt_atualiza)
		data_inicio_periodo = DateTools.converter_ano_mes_dia_para_string(dt_inicio)
		data_final_periodo = DateTools.converter_ano_mes_dia_para_string(dt_final)

		info(f'valores:{valores}')

		#iam = valores[1]
		#juros = valores[2]
		aplicar_selic = (selic == 'on')		
		lista_tabelas = ApiIndice.get_cod_nome_desc_das_tabelas()		
		tabela_pnep, tabela_juros = Utils.encontrar_valores_por_nome(lista_tabelas, iam, juros)

		iam_juros = Tabelas(tabela_juros=tabela_juros, 
							tabela_pnep=tabela_pnep,
							data_citacao=data_citacao,					#'01/09/1995',
							data_atualizacao=data_atualizacao,			#'30/06/2022',
							data_inicio_periodo=data_inicio_periodo,	#'21/07/1995',
							data_final_periodo=data_final_periodo, 		#'30/06/2022',
							aplicar_selic=aplicar_selic, 
							aplicar_selic_juros=True
							)
		
		sufixo = iam_juros.sufixo()
		
		if aplicar_selic:
			sufixo['selic_acumulada'] = sufixo['selic_acumulada'] * 100
		
		sufixo_lista = sufixo.to_dict(orient='records')  # Converte o DataFrame para uma lista de dicionários		
		return render(request, 'indices.html',{'tabelas':sufixo_lista, 'valores':valores, 'aplicar_selic':aplicar_selic})
		
		
	else:
		lista_tabelas = ApiIndice.get_lista_completa_das_tabelas()
	
		# teste = [[item[0], item[1], item[2]] for item in lista_tabelas if 200 <= item[0] < 400]
		# #info(f'teste:\n{teste}')
		lista_tabelas_indices = [item[1] for item in lista_tabelas if 200 <= item[0] < 300]
		lista_tabelas_juros = [item[1] for item in lista_tabelas if 300 < item[0] < 312]
		
		return render(request, 'indices.html',{'pnep':lista_tabelas_indices, 'juros': lista_tabelas_juros})











































def leitura(request):
	if request.method == 'POST':
		#lista_itens = list(dict(request.POST.items()))
		valores = list(dict(request.POST.items()).values())		
		""" 
		valores[1]= html, valores[2]= data_inicial,valores[3]= data_final
		valores[4]= 1 (pdf) ou 2(excel), valores[5]= nome da tabela
		"""		
		#info(f"items:\n{lista_itens}")
		#info(f"valores[4]:\n {valores[4]}")
		 
		# html, datainicial e datafinal
		df, cabecalhos = tabela_html_scraper(valores[1], valores[2], valores[3])
		if valores[4] == "1":
			resposta = gerarPDF_old(valores, cabecalhos, df)
			return resposta
		elif valores[4] == "2":
			resposta = gerarExcel(valores,cabecalhos, df)
			return resposta
				
	return render(request, 'leitura.html',{})

	











###############################################################################################


#===============================================================================
def teste(request):

	
	data = '234' #rotina_de_updload()
	

	lista_rubricas=["1111","2222", "3333", "4444","5555", "66666"]
	anoinicial="2002"
	anofinal ="2003"
	#faz chamada a api serpro
	
	

	return render(request,'sidenav.html',{'y':data})

def simple_upload(request, valor):
	#valor = 123456789

	return render(request, 'simple_upload.html', {'y':valor})

#================================================================================


def home(request):
	first_name = "DCP"
	last_name = "Brasília-DF"
	return render(request,'home.html',{})



def about(request):
	first_name = "DCP"
	last_name = "Brasília-DF"
	return render(request,'about.html',{'first_name':first_name,'last_name':last_name})


def gratificacoes(request):
	first_name = "DCP"
	last_name = "Brasília-DF"
	return render(request,'gratificacoes.html',{})


def especificos(request):
	first_name = "DCP"
	last_name = "Brasília-DF"
	return render(request,'especificos.html',{})

def gratifica_parametro(request):

	return render(request, 'gratifica_parametro.html',{})


def customizados(request):
	#from src.testsoap import lista_servico, calcula_prazo, funcao1

	#first_name = "DCP"
	#last_name = "Brasília-DF"
	#prazo = calcula_prazo("41432","70362010","70292070")
	
	#lista = lista_servico()
	#servico = resposta['cServicosCalculo']

	#listaservico ={'nome':'sobre','caldo':'212128','cep':21342309}
    
	return render(request,'customizados.html',{'num1':'lista'})



def lista(request):

	if request.method == "POST":
		form = ListForm(request.POST or None)

		if form.is_valid():
			form.save()
			all_items = List.objects.all
			messages.success(request, ('Item adicionado à lista'))
			return render(request, 'lista.html', {'all_items':all_items})

	else:	
		all_items = List.objects.all
		return render(request, 'lista.html', {'all_items':all_items})

def temporaria(request):

	if request.method == "POST":
		form = ListForm(request.POST or None)

		if form.is_valid():
			form.save()
			all_items = List.objects.all
			messages.success(request, ('Item adicionado à lista'))
			return render(request, 'temporaria.html', {'all_items':all_items})

	else:	
		all_items = List.objects.all
		return render(request, 'temporaria.html', {'all_items':all_items})


def delete(request, list_id):
	item = List.objects.get(pk=list_id)
	item.delete()
	messages.success(request, ('Item removido da lista'))
	return redirect('temporaria')	

def cross_off(request, list_id):
	item = List.objects.get(pk=list_id)
	item.completed = True
	item.save()
	return redirect('temporaria')	

def uncross(request, list_id):
	item = List.objects.get(pk=list_id)
	item.completed = False
	item.save()
	return redirect('temporaria')

def edit(request, list_id):
	if request.method == 'POST':
		item = List.objects.get(pk=list_id)

		form = ListForm(request.POST or None, instance=item)
        
		if form.is_valid():
			form.save()
			messages.success(request, ('Item editado!'))
			return redirect('temporaria')

	else:
		item = List.objects.get(pk=list_id)
		return render(request, 'edit.html', {'item': item})




