# services/retrieval.py
from db.queries import ensure_schema, search_similar

def search(query, top_k=3, source=None):
    ensure_schema()
    return search_similar(query=query, top_k=top_k, source=source)