import psycopg2

# Se o banco de dados não existir, ele será criado automaticamente
con = psycopg2.connect(
            dbname="ttrx",
            user="admin",
            password="Debatable-Grime-Herbicide-Research-Unknowing-Aviation3",
            host="provider.hurricane.akash.pub",
            port="30601"
)

# Cria um Cursor
sql = con.cursor()

sql.execute('''
             CREATE TABLE IF NOT EXISTS Admin (
                 id INTEGER PRIMARY KEY,
                 Link TEXT,
                 API TEXT,
                 Mod_Partner TEXT,
                 Mod_Product TEXT,
                 Mod_Outbound TEXT,
                 Mod_ByPicking TEXT,
                 Mod_Containers TEXT,
                 Mod_Quarantine TEXT,
                 Mod_RMA TEXT,
                 Mod_Com_Pack TEXT,
                 Mod_Disporsal TEXT,
                 Mod_Transformation TEXT
             )
''')