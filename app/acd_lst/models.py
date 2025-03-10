from django.db import models
from django import forms


class Document(models.Model):
    description = models.CharField(max_length=255, blank=True)
    document = models.FileField(upload_to='documents/')
    uploaded_at = models.DateTimeField(auto_now_add=True)


class TbBase317(models.Model):
	codigorubrica = models.IntegerField('Código')
	nomerubrica = models.CharField('Rubrica', max_length=200)
	tipo = models.CharField('Tipo', max_length=1)

	class Meta:
		db_table = 'tb_base317'
		verbose_name = 'Base Cálculo 3.17'
		verbose_name_plural = 'Base Cálculo 3.17'

	def __str__ (self):
		return f"{self.codigorubrica} - {self.nomerubrica} - {self.tipo}"
	
	
class TbBase2886(models.Model):
	codigorubrica = models.IntegerField('Código')
	nomerubrica = models.CharField('Rubrica', max_length=200)
	tipo = models.CharField('Tipo', max_length=1)

	class Meta:
		db_table = 'tb_base2886'
		verbose_name = 'Base Cálculo 28.86'
		verbose_name_plural = 'Base Cálculo 28.86'

	def __str__ (self):
		return f"{self.codigorubrica} - {self.nomerubrica} - {self.tipo}"

class AbateTeto(models.Model):
	codigorubrica = models.IntegerField('Código')
	nomerubrica = models.CharField('Rubrica', max_length=200)
	dtprimeirointervalo = models.CharField('Até janeiro 2004', max_length=1)
	dtsegundointervalo = models.CharField('A partir fevereiro 2004', max_length=1)

	class Meta:
		db_table = 'tb_abateteto'
		verbose_name = 'Base Cálculo Abate Teto'
		verbose_name_plural = 'Base Cálculo Abate Teto'

	def __str__ (self):
		return f"{self.codigorubrica} - {self.nomerubrica} - {self.dtprimeirointervalo}  - {self.dtsegundointervalo}"





# NOME_GRATIFICACAO = (
# 	('GDATA','GDATA'),
# 	('GDPGTAS','GDPGTAS'),
# 	('GDASST','GDASST'),
# 	('GDPGPE','GDPGPE'),
# 	)


# class CargoEmprego(models.Model):
# 	codcargo = models.CharField('Código',max_length=10)
# 	codgrupocargo = models.CharField('Grupo', max_length=10)
# 	nomecargo = models.CharField('Nome', max_length=200)
# 	nivel = models.CharField('Nível', max_length=10)

# 	class Meta:
# 		verbose_name = 'Cargo-Emprego'
# 		verbose_name_plural = 'Cargo-Emprego'

# 	def __str__ (self):
# 		return self.nomecargo + ' - ' + str(self.nivel)

# class OrgaoSiape(models.Model):
# 	codigo = models.CharField('Código', max_length=10)
# 	nome = models.CharField('Nome', max_length=200)

# 	class Meta:
# 		verbose_name = 'Órgão Siape'
# 		verbose_name_plural = 'Órgão Siape'

# 	def __str__ (self):
# 		return self.nome


# class Rubricas(models.Model):
# 	codigorubrica = models.CharField('Código', max_length=10)
# 	nomerubrica = models.CharField('Rubrica', max_length=200)

# 	class Meta:
# 		verbose_name = 'Rubrica'
# 		verbose_name_plural = 'Rubricas'

# 	def __str__ (self):
# 		return self.nomerubrica
	

class List (models.Model):
	item = models.CharField(max_length=200)
	completed = models.BooleanField(default=False)


	def __str__ (self):
		return self.item + ' ' + str(self.completed)



# class GratValorPonto(models.Model):
# 	nomegrat = models.CharField('Gratificação', max_length=10, choices=NOME_GRATIFICACAO)
# 	datainicio = models.CharField('Data de início',max_length=10)
# 	datafinal = models.CharField('Data final', max_length=10)
# 	nivel = models.CharField('Nível',max_length=3)
# 	classe = models.CharField('Classe', max_length=1)
# 	padrao = models.CharField('Padrão', max_length=1)
# 	valorponto = models.DecimalField('Valor do ponto', decimal_places=2, max_digits=8)

# 	class Meta:
# 		verbose_name = 'Valor do Ponto'
# 		verbose_name_plural = 'Valor do Ponto'



# class GratPontuacao(models.Model):
# 	nomegrat = models.CharField('Gratificação', max_length=10, choices=NOME_GRATIFICACAO)
# 	pontuacao = models.DecimalField('Pontuação',decimal_places=2,max_digits=5)
# 	datainicio = models.CharField('Data de início',max_length=10)
# 	datafinal = models.CharField('Data final', max_length=10)

# 	class Meta:
# 		verbose_name = 'Pontuação'
# 		verbose_name_plural = 'Pontuação'
	


