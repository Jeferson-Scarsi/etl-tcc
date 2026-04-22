import os

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