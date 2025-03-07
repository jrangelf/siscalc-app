import csv
import sqlite3
from collections import defaultdict

# Caminho para o banco de dados SQLite3 e o arquivo CSV
db_path = "/Volumes/2TB_P3SSD/siscalc/app-siscalc/app/db.sqlite3"  # Substitua pelo nome correto do arquivo SQLite, se necessário
csv_path = "/Volumes/2TB_P3SSD/siscalc/app-siscalc/rubricas-abateteto.csv"

# Conectar ao banco de dados SQLite3
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Verificar se a tabela existe (opcional, caso já esteja criada)
cursor.execute("""
CREATE TABLE IF NOT EXISTS tb_abateteto (
    codigorubrica TEXT,
    nomerubrica TEXT,
    dtprimeirointervalo TEXT,
    dtsegundointervalo TEXT
);
""")

# Ler o arquivo CSV
def ler_csv_e_inserir():
    codigos_repetidos = defaultdict(int)  # Para rastrear códigos repetidos
    linhas_para_inserir = []

    try:
        with open(csv_path, "r", encoding="utf-8") as arquivo_csv:
            leitor_csv = csv.reader(arquivo_csv, delimiter=";")
            next(leitor_csv)  # Ignorar o cabeçalho (CODIGO; DESCRICAO; até jan2004; a partir fev2004)

            for linha in leitor_csv:
                if len(linha) >= 4:  # Garantir que a linha tem os campos necessários
                    codigo = linha[0].strip()
                    descricao = linha[1].strip()
                    data1 = linha[2].strip()
                    data2 = linha[3].strip()

                    # Contar repetições de código
                    codigos_repetidos[codigo] += 1

                    # Adicionar à lista para inserção
                    linhas_para_inserir.append((codigo, descricao, data1, data2))

        # Exibir códigos repetidos, se houver
        for codigo, contagem in codigos_repetidos.items():
            if contagem > 1:
                print(f"Código repetido: {codigo} (aparece {contagem} vezes)")

        # Inserir dados no banco de dados
        cursor.executemany("""
        INSERT INTO tb_abateteto (codigorubrica, nomerubrica, dtprimeirointervalo, dtsegundointervalo)
        VALUES (?, ?, ?, ?)
        """, linhas_para_inserir)

        conn.commit()
        print("Dados inseridos com sucesso!")

    except Exception as e:
        print(f"Erro ao processar o arquivo CSV ou inserir dados: {e}")
    finally:
        conn.close()

# Executar a função principal
ler_csv_e_inserir()
