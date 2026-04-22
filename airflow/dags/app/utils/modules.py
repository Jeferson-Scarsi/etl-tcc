import psycopg2 as pg
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text 
from airflow.hooks.base import BaseHook


def get_connection(conn_id):
    try:
        connection = BaseHook.get_connection(conn_id)
        return connection.host, connection.schema, connection.port, connection.login, connection.password
    except Exception as e:
        raise(f"Erro ao obter conexão: {e}")

def connect_db(host, port, database, user, password):
    try:
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(url)
    except Exception as e:
        raise(f"Erro ao conectar ao banco: {e}")