import re
import pandas as pd
import psycopg2

def _validate_identifier(name: str) -> str:
    if not re.match(r'^[A-Za-z0-9_\.]+$', name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name

def connect(host: str, port: int, database: str, user: str, password: str):
    conn = psycopg2.connect(
        host=host,
        port=port,
        database=database,
        user=user,
        password=password
    )
    return conn

def list_tables(host: str, port: int, database: str, user: str, password: str) -> list:
    conn = connect(host, port, database, user, password)
    cursor = conn.cursor()
    cursor.execute("""
        SELECT table_name 
        FROM information_schema.tables 
        WHERE table_schema = 'public'
        ORDER BY table_name
    """)
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