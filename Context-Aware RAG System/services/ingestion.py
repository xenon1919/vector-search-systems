# services/ingestion.py
from db.queries import ensure_schema, insert_chunks

def store_chunks(chunks, source="default"):
    ensure_schema()
    return insert_chunks(chunks, source=source)