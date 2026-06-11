import pandas as pd
from elasticsearch import Elasticsearch

def connect(host: str, port: int, username: str = "", password: str = "", use_ssl: bool = False) -> Elasticsearch:
    scheme = "https" if use_ssl else "http"
    if username and password:
        return Elasticsearch(f"{scheme}://{username}:{password}@{host}:{port}", verify_certs=False)
    return Elasticsearch(f"{scheme}://{host}:{port}")

def list_indices(host: str, port: int, username: str = "", password: str = "", use_ssl: bool = False) -> list:
    es = connect(host, port, username, password, use_ssl)
    indices = sorted(i for i in es.indices.get_alias().keys() if not i.startswith("."))
    es.close()
    return indices

def fetch_index(host: str, port: int, index: str, username: str = "", password: str = "", use_ssl: bool = False, limit: int = 1000) -> pd.DataFrame:
    es = connect(host, port, username, password, use_ssl)
    response = es.search(index=index, query={"match_all": {}}, size=min(limit, 10000))
    hits = response["hits"]["hits"]
    es.close()
    if not hits:
        return pd.DataFrame()
    rows = [{"_id": h["_id"], **h["_source"]} for h in hits]
    return pd.DataFrame(rows)
