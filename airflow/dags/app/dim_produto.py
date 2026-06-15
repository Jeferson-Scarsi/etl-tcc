import os
import pandas as pd
import utils.modules as md

# Define a conexão com o banco de dados usando as variáveis de ambiente
# connection.host, connection.schema, connection.port, connection.login, connection.password
host_prd, db_prd, port_prd, user_prd, password_prd = md.get_connection("cnx_prd_ecommerce")
conn_prd = md.connect_db(host=host_prd,port=port_prd,database=db_prd,user=user_prd,password=password_prd)
host_dw, db_dw, port_dw, user_dw, password_dw = md.get_connection("cnx_dw_ecommerce")
conn_dw = md.connect_db(host=host_dw,port=port_dw,database=db_dw,user=user_dw,password=password_dw)


def dim_produto():
    # 1 - Busca o SQL do arquivo e faz a consulta no banco de dados
    sql = md.load_sql('dim_produto.sql')
    with conn_prd.connect() as connection_prd:
        df = pd.read_sql_query(sql, connection_prd)
    
    # 2 - Ordena os dados por todas as colunas para garantir a consistência na ordenação de forma ascendente
    df = df.sort_values(by=['id_produto', 'categoria', 'peso_produto', 'largura_cm', 'altura_cm', 'comprimento_cm'], ascending=True)

    # 3 - Remove as linhas duplicadas com base na coluna cpf_cnpj.
    df = df.drop_duplicates(subset=['id_produto'], keep='first')
    
    # 6 - Seleciona as colunas necessárias para a tabela de dimensão do cliente
    df = df.rename(columns={
        'peso_produto': 'peso_g',
    })
    df = df[['id_produto', 'categoria', 'peso_g', 'largura_cm', 'altura_cm', 'comprimento_cm']]

    # 7 - Insere os dados na tabela de dimensão do cliente no banco de dados
    with conn_dw.connect() as connection_dw:
        df.to_sql(schema='dw', name='dim_produto', con=connection_dw, if_exists='append', index=False)
