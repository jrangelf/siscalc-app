from django.contrib import admin
from .models import *


@admin.register(TbBase317)
class TbBase317Admin(admin.ModelAdmin):
	list_display = ('codigorubrica', 'nomerubrica', 'tipo')
	search_fields = ('codigorubrica', 'nomerubrica')
	ordering = ('codigorubrica',)

@admin.register(TbBase2886)
class TbBase2886Admin(admin.ModelAdmin):
	list_display = ('codigorubrica', 'nomerubrica', 'tipo')
	search_fields = ('codigorubrica', 'nomerubrica')
	ordering = ('codigorubrica',)
	

@admin.register(AbateTeto)
class AbateTetoAdmin(admin.ModelAdmin):
	list_display = ('codigorubrica', 'nomerubrica', 'dtprimeirointervalo', 'dtsegundointervalo')
	search_fields = ('codigorubrica', 'nomerubrica')
	ordering = ('codigorubrica',)	




# class RubricasAdmin(admin.ModelAdmin):
# 	list_display = ['codigorubrica', 'nomerubrica']
# 	orderby = ['codigorubrica']

# class GratValorPontoAdmin(admin.ModelAdmin):
# 	list_display = ('nomegrat','datainicio','datafinal','nivel','classe','padrao','valorponto')

# class GratPontuacaoAdmin(admin.ModelAdmin):
# 	list_display = ('nomegrat','pontuacao','datainicio','datafinal')

# class CargoEmpregoAdmin(admin.ModelAdmin):
# 	list_display = ('codcargo','codgrupocargo','nomecargo', 'nivel')

# class OrgaoSiapeAdmin(admin.ModelAdmin):
# 	list_display = ('codigo','nome')
# 	orderby = ['nome']




# class T01TabelaDCPAdmin(admin.ModelAdmin):
# 	list_display = ('t01_data','t01_cod_indexador','t01_var_per_mensal','t01_num_indice_var_mensal','t01_fator_vigente','t01_indice_correcao')
# 	ordering = ['t01_data']

# class T02TabelaDCPAdmin(admin.ModelAdmin):
# 	list_display = ('t02_data','t02_cod_indexador','t02_var_per_mensal','t02_num_indice_var_mensal','t02_fator_vigente','t02_indice_correcao')
# 	ordering = ['t02_data']




admin.site.register(List)


# admin.site.register(OrgaoSiape,OrgaoSiapeAdmin)
# admin.site.register(Rubricas, RubricasAdmin)
# admin.site.register(GratValorPonto, GratValorPontoAdmin)
# admin.site.register(GratPontuacao, GratPontuacaoAdmin)

# admin.site.register(T21ListaTabelasDCP,T21ListaTabelasDCPAdmin)

# admin.site.register(T01TabelaDCP,T01TabelaDCPAdmin)
# admin.site.register(T02TabelaDCP,T02TabelaDCPAdmin)
# admin.site.register(T03TabelaDCP,T03TabelaDCPAdmin)
# admin.site.register(T04TabelaDCP,T04TabelaDCPAdmin)
# admin.site.register(T05TabelaDCP,T05TabelaDCPAdmin)
# admin.site.register(T06TabelaDCP,T06TabelaDCPAdmin)
# admin.site.register(T07TabelaDCP,T07TabelaDCPAdmin)
# admin.site.register(T08TabelaDCP,T08TabelaDCPAdmin)
# admin.site.register(T09TabelaDCP,T09TabelaDCPAdmin)
# admin.site.register(T10TabelaDCP,T10TabelaDCPAdmin)
# admin.site.register(T11TabelaDCP,T11TabelaDCPAdmin)
# admin.site.register(T12TabelaDCP,T12TabelaDCPAdmin)
# admin.site.register(T13TabelaDCP,T13TabelaDCPAdmin)
# admin.site.register(T14TabelaDCP,T14TabelaDCPAdmin)
# admin.site.register(T15TabelaDCP,T15TabelaDCPAdmin)


# admin.site.register(T21TabelaDCP,T21TabelaDCPAdmin)
# admin.site.register(T22TabelaDCP,T22TabelaDCPAdmin)
# admin.site.register(T23TabelaDCP,T23TabelaDCPAdmin)