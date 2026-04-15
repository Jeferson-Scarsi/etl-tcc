import psycopg2 as pg
from dotenv import load_dotenv
import os
from sqlalchemy import create_engine, text 

def connect_db(host, port, database, user, password):
    try:
        url = f"postgresql://{user}:{password}@{host}:{port}/{database}"
        return create_engine(url)
    except Exception as e:
        print(f"Erro ao conectar ao banco: {e}")
        return None