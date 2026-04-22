from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

from app.dim_pagamento import dim_pagamento
from app.dim_cliente import dim_cliente


with DAG(
    dag_id='dag_ecommerce',
    start_date=datetime(2026, 4, 15),
    schedule='@daily',
    catchup=False,
    tags=["ecommerce"],
) as dag:
    
    inicio = EmptyOperator(task_id='inicio')

    dim_pagamento = PythonOperator(
            task_id='dim_pagamento',
            python_callable=dim_pagamento
        )

    inicio >> dim_pagamento