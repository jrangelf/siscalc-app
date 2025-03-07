from django.urls import path
from . import views


urlpatterns = [
	path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('delete/<list_id>', views.delete, name='delete'),
    path('cross_off/<list_id>', views.cross_off, name='cross_off'),
    path('uncross/<list_id>', views.uncross, name='uncross'),
    path('rubricas/', views.rubricas, name='rubricas'),
    path('rubricas-lista/', views.rubricaslista, name='rubricas-lista'),
    path('ficha/', views.ficha, name='ficha'),
    path('ficha-lista/', views.fichalista, name='ficha-lista'),
    path('lista/', views.lista, name='lista'),
    path('lista/temporaria/', views.temporaria, name='temporaria'),
    path('obitos/', views.obitos, name='obitos'),
    path('obitos-lista/', views.obitoslista, name='obitos-lista'),
    path('gratificacoes/', views.gratificacoes, name='gratificacoes'),
    path('especificos/', views.especificos, name='especificos'),
    path('customizados/', views.customizados, name='customizados'),
    path('tabelas/', views.tabelaspnep, name='tabelaspnep'),
    path('tabelas-lista/', views.tabelaspnep_lista, name='tabelas-lista'),    
    path('testnav/', views.teste, name='teste'),
    path('simple/<valor>', views.simple_upload, name='simple'),
    path('gratifica_parametro/', views.gratifica_parametro, name='gratifica_parametro'),
    path('leitura/', views.leitura, name='leitura'),
    path('edit/<list_id>', views.edit, name='edit'),
    path('calculo317/', views.calculo317, name='calculo317'),
    path('resultado317/', views.resultado317, name='resultado317'),
    path('calculo2886/', views.calculo2886, name='calculo2886'),
    path('resultado2886/', views.resultado2886, name='resultado2886'),
    path('indices/', views.indices, name='indices'), 
    path('resumo/', views.resumo, name='resumo'),    
 
]