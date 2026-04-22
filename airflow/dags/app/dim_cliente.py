import os
import pandas as pd
# os.path.join(os.path.dirname(__file__), '..', 'modules.py')
import app.utils.modules as modules


def dim_cliente():
    sql = """
    SELECT pi.status_pedido
      FROM producao.pedidos pi
    """

    conn = modules.connect_db(
        host=os.getenv("OLIST_PRD_HOST"),
        port=os.getenv("OLIST_PRD_PORT"),
        database=os.getenv("OLIST_PRD_DB"),
        user=os.getenv("OLIST_PRD_USER"),
        password=os.getenv("OLIST_PRD_PASSWORD")
    )

    with conn.connect() as connection:
        df = pd.read_sql_query(sql, connection)
    
    print(df.head())