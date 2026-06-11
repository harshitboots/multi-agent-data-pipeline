import re
import pandas as pd
from databricks import sql
from databricks.sdk import WorkspaceClient

def _validate_identifier(name: str) -> str:
    if not re.match(r'^[A-Za-z0-9_\.]+$', name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name

def connect(host: str, token: str, http_path: str):
    conn = sql.connect(
        server_hostname=host,
        http_path=http_path,
        access_token=token
    )
    return conn

def list_tables(host: str, token: str, http_path: str) -> list:
    conn = connect(host, token, http_path)
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES")
    tables = [row[1] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def fetch_table(host: str, token: str, http_path: str, table: str, limit: int = 1000) -> pd.DataFrame:
    conn = connect(host, token, http_path)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {_validate_identifier(table)} LIMIT {limit}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)