import re
import pandas as pd
import duckdb

def _validate_identifier(name: str) -> str:
    if not re.match(r'^[A-Za-z0-9_\.]+$', name):
        raise ValueError(f"Invalid identifier: {name!r}")
    return name

def connect(filepath: str):
    return duckdb.connect(filepath)

def list_tables(filepath: str) -> list:
    conn = connect(filepath)
    result = conn.execute("SHOW TABLES").fetchall()
    conn.close()
    return [row[0] for row in result]

def fetch_table(filepath: str, table: str, limit: int = 1000) -> pd.DataFrame:
    conn = connect(filepath)
    df = conn.execute(f"SELECT * FROM {_validate_identifier(table)} LIMIT {limit}").df()
    conn.close()
    return df
