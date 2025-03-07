from datetime import datetime
from django.utils.encoding import force_str
from acd_lst.models import *
from src.configura_debug import *

def montar_tabela(titulo, observacao, tabela, codigo):
    
    #info(f"numero colunas: {tabela}")
    
    lista = []
    listaL = []
    comprimento = len(tabela)        
    data_atualiza = tabela[-1]['data']    
    numero_colunas = len(tabela[0]) - 1

    if numero_colunas == 6:

        """
        Dicionário específico para as tabelas índices PNEP:
        {
        'tabela': titulo_da_tabela, 
        'lista': [linha_da_tabela],
        'data_atualizacao': data (date),
        'tamanho': tamanho (int),
        'descricao': observacao (str)    
        }
        lista = [
            ID,
            DATA, 
            INDEXADOR, 
            VAR_PERC MENSAL, 
            NUM_INDICE_VAR_MENSAL, 
            FATOR_VIGENTE, 
            INDICE_CORRECAO]
        """               
         
        for i in range(len(tabela)):
            listaL.append(i)            
            listaL.append(tabela[i]['data']) 
            listaL.append(tabela[i]['indexador']) 
            listaL.append(tabela[i]['variacao_mensal']) 
            listaL.append(tabela[i]['numero_indice']) 
            listaL.append(tabela[i]['fator_vigente']) 
            listaL.append(tabela[i]['indice_correcao']) 
            lista.append(listaL)            
            listaL = []       
        
        return {'tabela':titulo,
                'lista':lista,
                'data_atualizacao':data_atualiza,
                'tamanho':comprimento,
                'descricao':observacao,            
                'colunas': numero_colunas,
                'codigo' : codigo}

    if numero_colunas == 4:

        """
        Dicionário específico para as tabelas juros SELIC:
        {
        'tabela': titulo_da_tabela, 
        'lista': [linha_da_tabela],
        'data_atualizacao': data (date),
        'tamanho': tamanho (int),
        'descricao': observacao (str)    
        }
        lista = [
            ID,
            DATA, 
            SELIC, 
            SELIC ACUMULADA,
            SELIC ACUMULADA MENSAL]
        """               
         
        for i in range(len(tabela)):
            listaL.append(i)
            selic = tabela[i]['selic']
            selicacumulada = tabela[i]['selic_acumulada'] 
            selicacumuladamensal = tabela[i]['selic_acumulada_mensal']
            if selic is not None:
                selic *= 100
            if selicacumulada is not None:
                selicacumulada *= 100
            if selicacumuladamensal is not None:
                selicacumuladamensal *= 100
            listaL.append(tabela[i]['data']) 
            listaL.append(selic) 
            listaL.append(selicacumulada) 
            listaL.append(selicacumuladamensal)
            lista.append(listaL)            
            listaL = []       
        
        return {'tabela':titulo,
                'lista':lista,
                'data_atualizacao':data_atualiza,
                'tamanho':comprimento,
                'descricao':observacao,            
                'colunas': numero_colunas,
                'codigo': codigo}

    if numero_colunas == 2:

        """
        Dicionário específico para as tabelas indexadores Banco Central 
        {
        'tabela': titulo_da_tabela, 
        'lista': [linha_da_tabela],
        'data_atualizacao': data (date),
        'tamanho': tamanho (int),
        'descricao': observacao (str)    
        }
        lista = [
            ID,
            DATA, 
            VALOR]
        """               
         
        for i in range(len(tabela)):
            listaL.append(i)            
            listaL.append(tabela[i]['data']) 
            listaL.append(tabela[i]['valor']) 
            lista.append(listaL)            
            listaL = []       
        
        return {'tabela':titulo,
                'lista':lista,
                'data_atualizacao':data_atualiza,
                'tamanho':comprimento,
                'descricao':observacao,            
                'colunas': numero_colunas,
                'codigo' : codigo}
    
    if numero_colunas == 3:

        """
        Dicionário específico para as tabelas de juros, exceto SELIC:
        {
        'tabela': titulo_da_tabela, 
        'lista': [linha_da_tabela],
        'data_atualizacao': data (date),
        'tamanho': tamanho (int),
        'descricao': observacao (str)    
        }
        lista_poupanca = [
            ID,
            DATA, 
            META SELIC COPOM,
            VALOR]

        lista = [
            ID,
            DATA, 
            JUROS MENSAIS,
            JUROS ACUMULADOS]                
        """               
         
        for i in range(len(tabela)):
            listaL.append(i)            
            listaL.append(tabela[i]['data'])
            if codigo == 300:
                metaselic = tabela[i]['meta_selic_copom']
                if metaselic is not None:
                    metaselic *= 100
                taxamensal = tabela[i]['taxa_mensal']
                if taxamensal is not None:
                    taxamensal *= 100
                listaL.append(metaselic)
                listaL.append(taxamensal)
                #listaL.append(tabela[i]['meta_selic_copom']) 
                #listaL.append(tabela[i]['taxa_mensal'])
            else:
                jurosmensal = tabela[i]['juros_mensal']
                if jurosmensal is not None:
                    jurosmensal *= 100
                jurosacumulados = tabela[i]['juros_acumulados']
                if jurosacumulados is not None:
                    jurosacumulados *= 100                
                listaL.append(jurosmensal)
                listaL.append(jurosacumulados)
                #listaL.append(tabela[i]['juros_mensal']) 
                #listaL.append(tabela[i]['juros_acumulados'])
            
            lista.append(listaL)
            listaL = []       
        
        return {'tabela':titulo,
                'lista':lista,
                'data_atualizacao':data_atualiza,
                'tamanho':comprimento,
                'descricao':observacao,            
                'colunas': numero_colunas,
                'codigo': codigo}

    return None        
