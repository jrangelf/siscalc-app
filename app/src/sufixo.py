from acd_indices_calculo import MatrizIndices
import pandas as pd

iam_juros = MatrizIndices(
    tabela_juros='t302_juros',
    tabela_pnep='t200_tabela_pnep',
    data_citacao='01/09/1995',
    data_atualizacao='30/06/2022',
    data_inicio_periodo='21/07/1995',
    data_final_periodo='30/06/2022',
    aplicar_selic=True,
    aplicar_selic_juros=True
)

juros = iam_juros.juros()
indice = iam_juros.indice()
selic = iam_juros.selic()
sufixo = iam_juros.sufixo()

# Exibir o DataFrame final
pd.set_option('display.max_rows', None)
pd.set_option("display.float_format", "{:.8f}".format)

print("Juros:\n", juros)
print("\nÍndice:\n", indice)
print("\nSELIC:\n", selic)
print("\nSufixo:\n", sufixo)






