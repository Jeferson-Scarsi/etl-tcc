import psycopg2 as pg
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text 
from airflow.sdk.bases.hook import BaseHook


def get_connection(conn_id):
    try:
        connection = BaseHook.get_connection(conn_id)
        return connection.host, connection.schema, connection.port, connection.login, connection.password
    except Exception as e:
        raise RuntimeError(f"Erro ao obter conexão: {e}") from e

def connect_db(host, port, database, user, password):
    try:
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(url)
    except Exception as e:
        raise RuntimeError(
            f"Erro ao conectar ao banco. "
            f"host={host}, port={port}, database={database}, user={user}. "
            f"Erro original: {e}"
        ) from e

def load_sql(nome_arquivo):
    """
    Carrega um arquivo SQL da pasta /dags/sql
    """

    caminho_sql = os.path.join(
        os.path.dirname(__file__),  # utils/
        "../sql",                # sobe até dags/sql
        nome_arquivo
    )

    caminho_sql = os.path.abspath(caminho_sql)

    if not os.path.exists(caminho_sql):
        raise FileNotFoundError(f"SQL não encontrado: {caminho_sql}")

    with open(caminho_sql, "r", encoding="utf-8") as f:
        return f.read()