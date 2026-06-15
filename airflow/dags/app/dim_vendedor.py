import os
import pandas as pd
import utils.modules as md

# Define a conexão com o banco de dados usando as variáveis de ambiente
# connection.host, connection.schema, connection.port, connection.login, connection.password
host_prd, db_prd, port_prd, user_prd, password_prd = md.get_connection("cnx_prd_ecommerce")
conn_prd = md.connect_db(host=host_prd,port=port_prd,database=db_prd,user=user_prd,password=password_prd)
host_dw, db_dw, port_dw, user_dw, password_dw = md.get_connection("cnx_dw_ecommerce")
conn_dw = md.connect_db(host=host_dw,port=port_dw,database=db_dw,user=user_dw,password=password_dw)


def dim_vendedor():
    # 1 - Busca o SQL do arquivo e faz a consulta no banco de dados
    sql = md.load_sql('dim_vendedor.sql')
    with conn_prd.connect() as connection_prd:
        df = pd.read_sql_query(sql, connection_prd)
        
    # 4 - Ordena os dados por todas as colunas para garantir a consistência na ordenação de forma ascendente
    df = df.sort_values(by=['seller_id', 'seller_city', 'seller_state'], ascending=True)

    # 5 - Remove as linhas duplicadas com base na coluna seller_id.
    df = df.drop_duplicates(subset=['seller_id'], keep='first')
    
    # 6 - Seleciona as colunas necessárias para a tabela de dimensão do cliente
    df = df[['seller_id', 'seller_city', 'seller_state']]

    # 7 - Insere os dados na tabela de dimensão do cliente no banco de dados
    df_colunas = {
        'seller_id': 'id_vendedor',
        'seller_city': 'cidade',
        'seller_state': 'estado'
    }
    df = df.rename(columns=df_colunas)
    with conn_dw.connect() as connection_dw:
        df.to_sql(schema='dw', name='dim_vendedor', con=connection_dw, if_exists='append', index=False)
