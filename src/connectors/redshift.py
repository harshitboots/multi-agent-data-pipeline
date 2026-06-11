import re
import pandas as pd
import redshift_connector

def _validate_identifier(name: str) -> str:
    if not re.match(r'^[A-Za-z0-9_\.]+$', name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name

def connect(host: str, port: int, database: str, user: str, password: str):
    return redshift_connector.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )

def list_tables(host: str, port: int, database: str, user: str, password: str) -> list:
    conn = connect(host, port, database, user, password)
    cursor = conn.cursor()
    cursor.execute("SELECT tablename FROM pg_catalog.pg_tables WHERE schemaname='public' ORDER BY tablename")
    tables = [row[0] for row in cursor.fetchall()]
    cursor.close()
    conn.close()
    return tables

def fetch_table(host: str, port: int, database: str, user: str, password: str, table: str, limit: int = 1000) -> pd.DataFrame:
    conn = connect(host, port, database, user, password)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {_validate_identifier(table)} LIMIT {limit}")
    columns = [desc[0] for desc in cursor.description]
    rows = cursor.fetchall()
    cursor.close()
    conn.close()
    return pd.DataFrame(rows, columns=columns)
