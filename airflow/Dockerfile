FROM apache/airflow:3.2.0

USER root

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*
    && RUN pip install --no-cache-dir PyYAML

USER airflow

RUN pip install --no-cache-dir \
    psycopg2-binary \
    pandas \
    sqlalchemy \
    python-dotenv \
    dag-factory \
    sqlalchemy