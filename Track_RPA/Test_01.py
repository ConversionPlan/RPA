import sqlite3

# Se o banco de dados não existir, ele será criado automaticamente
con = sqlite3.connect('TWBD_01')

# Cria um Cursor
sql = con.cursor()

# # Cria a Query
# sql.execute('''
#     CREATE TABLE IF NOT EXISTS Admin (
#         id INTEGER PRIMARY KEY,
#         Link TEXT,
#         API TEXT,
#         Mod_Partner TEXT,
#         Mod_Product TEXT,
#         Mod_Outbound TEXT,
#         Mod_ByPicking TEXT,
#         Mod_Containers TEXT,
#         Mod_Quarantine TEXT,
#         Mod_RMA TEXT,
#         Mod_Com_Pack TEXT,
#         Mod_Disporsal TEXT,
#         Mod_Transformation TEXT
#     )
# ''')

# # Executa o Comando
# con.commit()

# # Inserir dados na tabela
# sql.execute("INSERT INTO Admin (Link, API, Mod_Partner, Mod_Product, Mod_Outbound, Mod_ByPicking, Mod_Containers, Mod_Quarantine, Mod_RMA, Mod_Com_Pack, Mod_Disporsal, Mod_Transformation) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", ("Link_02", "API Key", "T", "T", "T", "T", "T", "T", "T", "T", "T", "T"))
#
# # Executa o Comando
# con.commit()

# # Excluir dados na tabela
# sql.execute("DELETE FROM Admin WHERE id = 2")
#
# # Executa o Comando
# con.commit()

# Selecionar todos os Registros da Tabela
sql.execute("SELECT * FROM Admin")
regis = sql.fetchall()

print("Registros encontrados:", len(regis))

for r in regis:
    print(r)

# # Consultar um registro específico com base em uma condição (por exemplo, nome igual a "Alice")
# nome_procurado = "Link_02"
# sql.execute("SELECT * FROM Admin WHERE Link=?", (nome_procurado,))
# regis = sql.fetchone()
#
# if regis:
#     print("Registro encontrado:", regis)
#     # Acesso aos valores específicos do registro
#     id, Link, API, Mod_Partner, Mod_Product, Mod_Outbound, Mod_ByPicking, Mod_Containers, Mod_Quarantine, Mod_RMA, Mod_Com_Pack, Mod_Disporsal, Mod_Transformation = regis
#     print("Link:", Link)
#     print("API:", API)
# else:
#     print("Nenhum registro encontrado para o nome", nome_procurado)

con.close()
