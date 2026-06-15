import os
import pandas as pd
import utils.modules as md
from sqlalchemy import text

# Define a conexão com o banco de dados usando as variáveis de ambiente
# connection.host, connection.schema, connection.port, connection.login, connection.password
host_prd, db_prd, port_prd, user_prd, password_prd = md.get_connection("cnx_prd_ecommerce")
conn_prd = md.connect_db(host=host_prd,port=port_prd,database=db_prd,user=user_prd,password=password_prd)
host_dw, db_dw, port_dw, user_dw, password_dw = md.get_connection("cnx_dw_ecommerce")
conn_dw = md.connect_db(host=host_dw,port=port_dw,database=db_dw,user=user_dw,password=password_dw)

cd_origem_sistema = 2
with conn_dw.connect() as connection_dw:
    sql_config = "SELECT DISTINCT nr_contador + 1 as cd_execucao FROM config.contador WHERE desc_contador = 'contador_execucao'"
    df_execucao = pd.read_sql_query(sql_config, connection_dw)

def stg_vendas():
    total_processado = 0
    
    print("Iniciando processo de carga da tabela fato_venda...")
    # 1 - Busca o SQL do arquivo e faz a consulta no banco de dados
    sql = md.load_sql('stg_vendas.sql')
    with conn_prd.connect() as connection_prd:
        for df in pd.read_sql_query(sql, connection_prd, chunksize=10000):
            # 2 - Ordena os dados por todas as colunas para garantir a consistência na ordenação de forma ascendente
            df = df.sort_values(by=['id_pedido', 'id_cliente', 'id_produto', 'id_vendedor', 'dt_movimento'], ascending=True)

            # 3 - Remove as linhas duplicadas com base na coluna seller_id.
            df_fato = df.drop_duplicates(subset=['id_cliente', 'id_produto', 'id_vendedor', 'id_pedido', 'id_item_pedido'], keep='first')

            # 4 - Seleciona as colunas necessárias para a tabela de fato de venda
            df = df_fato[['id_cliente', 'id_produto', 'id_vendedor', 'status_pedido', 'id_pedido', 'id_item_pedido', 'vl_movimento', 
                          'vl_movimento_frete', 'dt_movimento', 'dt_aprovacao', 'dt_entrega_cliente']]

            # 5 - Mapeia as colunas e insere os dados na tabela de stage de venda no banco de dados
            with conn_dw.connect() as connection_dw:
                if total_processado == 0:
                    print("Limpando tabela stage.stg_vendas...")
                    connection_dw.execute(text("TRUNCATE TABLE stage.stg_venda"))
                    connection_dw.commit()
                df.to_sql(schema='stage', name='stg_venda', con=connection_dw, if_exists='append', chunksize=10000, index=False)

            total_processado += len(df)

            print(f"Lote commitado. Total processado: {total_processado}")