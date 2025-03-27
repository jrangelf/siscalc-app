from src.acd_api_serpro import MatrizSerpro
from src.acd_serpro_calculo import TabelasSerpro


class Calculos:

    @classmethod
    def calcular_2886_sicape(cls,
                             simplificado,
                             completo,
                             resultado):
        
        
        
        # montar um dicionário de dataframes para cada cpf de exequente
        results = TabelasSerpro.tabela_2886_sicape(simplificado, completo, resultado)
        
        # buscar Iam, juros, selic
        # aplicar teto
        # aplicar percentuais
        # aplicar pro-rata
        # aplicar segundo percentual.


        

    





        return


    
    
    
    
    
    
    
    
    
    
    def calcular_317_sicape(cls,a,b):
        ...