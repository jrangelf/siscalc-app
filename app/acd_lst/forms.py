from django import forms
from tempus_dominus.widgets import DatePicker
from datetime import datetime
from .models import List #, CargoEmprego, OrgaoSiape, Rubricas
from src.validacao import *


# class CargoEmpregoForm(forms.ModelForm):
# 	class Meta:
# 		model = CargoEmprego
# 		fields = ["codcargo","codgrupocargo","nomecargo","nivel"]


# class OrgaoSiapeForm(forms.ModelForm):
# 	class Meta:
# 		model = OrgaoSiape
# 		fields = ["codigo","nome"]


# class RubricasForm(forms.ModelForm):
# 	class Meta:
# 		model = Rubricas
# 		fields = ["codigorubrica","nomerubrica"]


class ListForm(forms.ModelForm):
	class Meta:
		model = List
		fields= ["item", "completed"]


class ObitoForm(forms.Form):
	numero_cpf = forms.CharField (label='CPF', max_length=14,required=False)
	varios_cpf = forms.CharField (label='Lista de CPFs (Máx: 500)', max_length=8000, widget=forms.Textarea(),required=False)
	
	#nome_arquivo = forms.FileField (label='Arquivo texto', max_length=100,required=False)
	# colocar 7500
	"""
	def clean(self):
		numero_cpf = self.cleaned_data.get('numero_cpf')
		varios_cpf = self.cleaned_data.get('varios_cpf')
		#nome_arquivo = self.cleaned_data.get('nome_arquivo')

		print("#-------------------------------------------------")
		print ('# numero_cpf=> ',numero_cpf)
		print ('# varios_cpf=>', varios_cpf)
		print ('# nome_arquivo=> ',nome_arquivo)
		print("#-------------------------------------------------")

		lista_de_erros = {}
		listacpf = {}
		modulo = 'Verificação de óbitos - '

		verifica_campos_entrada(numero_cpf, nome_arquivo, varios_cpf, lista_de_erros)
		
		verifica_nome_arquivo (nome_arquivo,'nome_arquivo',lista_de_erros)

		cpf=''
		nome_do_campo = ''

		if numero_cpf == "" and varios_cpf != "":
			cpf = varios_cpf
			nome_do_campo = 'varios_cpf'
		if numero_cpf !="" and varios_cpf == "":
			cpf = numero_cpf
			nome_do_campo = 'numero_cpf'

		listacpf = verifica_validade_cpf(cpf, nome_do_campo,lista_de_erros,modulo)

		# colocar junto o argumento varios cpf para fazer testes juntos.
		print("#-----------------forms.py--------------------------")
		print ("# listacpf: ",listacpf)
		print("#")
		print ("# lista_de_erros: ", lista_de_erros)
		print("#-------------------------------------------------")
		
		if lista_de_erros is not None:
			for erro in lista_de_erros:
				mensagem_erro = lista_de_erros[erro]
				print("#----------------forms.py-------------------------")
				print("# erro: ", erro)
				print("#")
				print("# mensagem_erro: ", mensagem_erro)
				print("#-------------------------------------------------")
				self.add_error(erro,mensagem_erro)				

		return self.cleaned_data
		"""
	
class RubricasForm(forms.Form):

	anoinicial = forms.CharField (label='Ano inicial', max_length=4,required=True)
	anofinal = forms.CharField (label='Ano final', max_length=4,required=True)
	orgao = forms.CharField (label='Órgão', max_length=8,required=False)		
	rubrica1 = forms.CharField (label='', max_length=6,required=False)
	rubrica2 = forms.CharField (label='',max_length=6,required=False)
	rubrica3 = forms.CharField (label='',max_length=6,required=False)
	rubrica4 = forms.CharField (label='',max_length=6,required=False)
	rubrica5 = forms.CharField (label='',max_length=6,required=False)
	rubrica6 = forms.CharField (label='',max_length=6,required=False)
	rubrica7 = forms.CharField (label='',max_length=6,required=False)
	rubrica8 = forms.CharField (label='',max_length=6,required=False)
	rubrica9 = forms.CharField (label='',max_length=6,required=False)
	rubrica10 = forms.CharField (label='',max_length=6,required=False)
	cpfs = forms.CharField (label='Lista de CPFs (Máx: 500)', max_length=8000, widget=forms.Textarea(),required=True)
	


class UploadFileForm(forms.Form):
    title = forms.CharField(label='Title:', max_length=50)
    file = forms.FileField(label='Arquivo: ',max_length=100)
