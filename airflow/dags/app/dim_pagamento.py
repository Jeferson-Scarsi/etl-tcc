import os
import pandas as pd
import psycopg2 as pg
from app.utils.sql_loader import load_sql
import app.utils.modules as modules

# Busca as conexões do banco de dados a partir das configuração
host_dw, schema_dw, port_dw, user_dw, password_dw = modules.get_connection('cnx_dw_ecommerce')
host_prd, schema_prd, port_prd, user_prd, password_prd = modules.get_connection('cnx_prd_ecommerce')
    
conn_prd = modules.connect_db(host=host_prd,port=port_prd,database=schema_prd,user=user_prd,password=password_prd)
conn_dw = modules.connect_db(host=host_dw,port=port_dw,database=schema_dw,user=user_dw,password=password_dw)

def dim_pagamento():
    # Table Input
    sql = load_sql('dim_pagamento.sql')   
    arquivo_sql = 'dim_pagamento.sql'
    caminho_sql = os.path.join(os.path.dirname(__file__), f'sql/{arquivo_sql}')
    with open(caminho_sql, 'r') as file:
        sql = file.read()

    with conn_prd.connect() as cnx_prd:
       df = pd.read_sql_query(sql, cnx_prd)
    
    # Select Values e Renomeia a coluna do DataFrame
    df = df.rename(columns={'status_pagamento': 'payment_type'})

    # Ordena as colunas do DataFrame
    df = df.sort_values(by=['payment_type'], ascending=[True])

    # Unique Rows
    df_final = df.drop_duplicates()

    # Insert Rows

    with conn_dw.connect() as cnx_dw:
        pd.to_sql(df_final, cnx_dw, if_exists='replace', index=False)