"""
agrupadas = [

{'codorgao': 17000, 'datas': [{'datapagto': 200801, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2030.16}]},
				               {'datapagto': 200802, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200803, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200804, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
   				               {'datapagto': 200805, 'ingressos': [
                                                                    {'codrubrica': 1, 'R': 2673.24},
                                                                    {'codrubrica': 13, 'R': 400.98},
                                                                    {'codrubrica': 136, 'R': 161.99},
                                                                    {'codrubrica': 31908, 'D': 2130.16}]},
                               {'datapagto': 200806, 'ingressos': []},
                               {'datapagto': 200807, 'ingressos': []},
                                                 .
                                                 .
                                                 .
                               {'datapagto': 200910, 'ingressos': []},
                               {'datapagto': 200911, 'ingressos': []},
                               {'datapagto': 200912, 'ingressos': []}]}]                                                         

                                          

exequentes = [{exequente_dict}, {exequente_dict},....,{exequente_dict}]
exequente_dict = {'cpf': '23413463401', 'orgaos': orgaos_lista}

agrupadas = [{orgao_dict},...{orgao_dict}]
orgao_dict = {'codorgao':22000, 'datas': datas}

datas = [{data_dict}, {data_dict},...{data_dict}]
data_dict = {'datapagto':200801, 'ingressos': ingressos}

ingressos = [{rubricas_dict},{rubricas_dict}...{rubricas_dict}]
rubricas_dict = {'codrubrica':13, 'R': 234.23, 'D':125.22}

"""

class RubricasAgrupadas:

    def __init__(self, dados_extracao, rubricas_lista, orgaos_lista, ano_inicial, ano_final):
        self.dados_extracao = dados_extracao
        self.rubricas_lista = rubricas_lista
        self.orgaos_lista = orgaos_lista
        self.ano_inicial = ano_inicial
        self.ano_final = ano_final

    def calcular_soma_valores(self, itens):
        soma = sum(float(item['valor']) for item in itens)
        return soma

    def filtrar_receitas(self, orgao_int, anomes_int, codrubrica_int):
        return [item for item in self.dados_extracao if item['codorgao'] == orgao_int and
                                                     item['datapagto'] == anomes_int and
                                                     item['codrubrica'] == codrubrica_int and
                                                     item['rendimento'] == 1]

    def filtrar_descontos(self, orgao_int, anomes_int, codrubrica_int):
        return [item for item in self.dados_extracao if item['codorgao'] == orgao_int and
                                                     item['datapagto'] == anomes_int and
                                                     item['codrubrica'] == codrubrica_int and
                                                     item['rendimento'] == 2]

    def agrupar_rubricas(self):
        periodo = [f"{ano:04d}{mes:02d}" for ano in range(self.ano_inicial, self.ano_final + 1) for mes in range(1, 13)]
        agrupadas = []

        for orgao in self.orgaos_lista:
            orgao_int = int(orgao)
            orgao_dict = {'codorgao': orgao_int}
            datas = []

            for anomes in periodo:
                anomes_int = int(anomes)
                ingressos = []

                for codrubrica in self.rubricas_lista:
                    codrubrica_int = int(codrubrica)

                    receitas = self.filtrar_receitas(orgao_int, anomes_int, codrubrica_int)
                    descontos = self.filtrar_descontos(orgao_int, anomes_int, codrubrica_int)

                    rubricas_dict = {}

                    if receitas:
                        if len(receitas) == 1:
                            rubricas_dict['codrubrica'] = codrubrica_int
                            rubricas_dict['R'] = receitas[0]['valor']
                        else:
                            soma = self.calcular_soma_valores(receitas)
                            rubricas_dict['codrubrica'] = codrubrica_int
                            rubricas_dict['R'] = soma

                        ingressos.append(rubricas_dict)

                    if descontos:
                        if len(descontos) == 1:
                            rubricas_dict['codrubrica'] = codrubrica_int
                            rubricas_dict['D'] = descontos[0]['valor']
                        else:
                            #soma = sum(item['valor'] for item in descontos)
                            soma = self.calcular_soma_valores(descontos)
                            rubricas_dict['codrubrica'] = codrubrica_int
                            rubricas_dict['D'] = soma

                        ingressos.append(rubricas_dict)

                if ingressos:
                    data_dict = {'datapagto': anomes_int, 'ingressos': ingressos}
                    datas.append(data_dict)

            orgao_dict['datas'] = datas
            agrupadas.append(orgao_dict)

        return agrupadas
