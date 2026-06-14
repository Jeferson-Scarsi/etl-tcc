from airflow import DAG
from airflow.providers.standard.operators.empty import EmptyOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from app.dim_cliente import dim_cliente
from app.dim_pagamento import dim_pagamento
from app.dim_produto import dim_produto
from app.dim_status_pedido import dim_status_pedido
from app.dim_vendedor import dim_vendedor
from app.stg_vendas import stg_vendas
from app.stg_pagamentos import stg_pagamentos
from utils.modules import get_connection, connect_db
from datetime import datetime

with DAG(
    dag_id="ecommerce_dw",
    schedule=None,
    start_date=datetime(2026, 1, 1),    
    catchup=False,
) as dag:

    start = EmptyOperator(task_id="start")
    task_dim_cliente = PythonOperator(
        task_id="task_dim_cliente",
        python_callable=dim_cliente,
    )
    task_dim_produto = PythonOperator(
        task_id="task_dim_produto",
        python_callable=dim_produto,
    )
    task_dim_pagamento = PythonOperator(
        task_id="task_dim_pagamento",
        python_callable=dim_pagamento,
    )
    task_dim_status_pedido = PythonOperator(
        task_id="task_dim_status_pedido",
        python_callable=dim_status_pedido,
    )
    task_dim_vendedor = PythonOperator(
        task_id="task_dim_vendedor",
        python_callable=dim_vendedor,
    )
    task_stg_vendas = PythonOperator(
        task_id="task_stg_vendas",
        python_callable=stg_vendas,
    )
    task_stg_pagamentos = PythonOperator(
        task_id="task_stg_pagamentos",
        python_callable=stg_pagamentos,
    )
    task_fun_carga_fatos = SQLExecuteQueryOperator(
        task_id="fun_carga_fatos",
        conn_id="cnx_dw_ecommerce",
        sql="sql/fun_carga_fatos.sql",
    )
    end = EmptyOperator(task_id="end")

    tasks_dimensoes = [
        task_dim_cliente,
        task_dim_produto,
        task_dim_pagamento,
        task_dim_status_pedido,
        task_dim_vendedor,
    ]
    
    tasks_stages = [
        task_stg_vendas,
        task_stg_pagamentos,
    ]
    
    start >> tasks_dimensoes
    
    for task_stage in tasks_stages:
        tasks_dimensoes >> task_stage
    
    tasks_stages >> task_fun_carga_fatos >> end