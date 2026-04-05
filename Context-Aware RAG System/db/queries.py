from typing import Iterable

from config import settings
from db.connection import get_connection
from embeddings.model import get_embedding
from utils.helpers import to_pgvector


def ensure_schema() -> None:
	conn = get_connection()
	cur = conn.cursor()

	cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")
	cur.execute(
		f"""
		CREATE TABLE IF NOT EXISTS documents (
			id BIGSERIAL PRIMARY KEY,
			content TEXT NOT NULL,
			embedding VECTOR({settings.embedding_dimension}) NOT NULL,
			source TEXT NOT NULL DEFAULT 'default',
			created_at TIMESTAMP NOT NULL DEFAULT NOW()
		);
		"""
	)

	conn.commit()
	cur.close()
	conn.close()


def insert_chunks(chunks: Iterable[str], source: str = "default") -> int:
	conn = get_connection()
	cur = conn.cursor()

	inserted = 0
	for chunk in chunks:
		chunk_text = chunk.strip()
		if not chunk_text:
			continue

		embedding = get_embedding(chunk_text)
		cur.execute(
			"""
			INSERT INTO documents (content, embedding, source)
			VALUES (%s, %s::vector, %s)
			""",
			(chunk_text, to_pgvector(embedding), source),
		)
		inserted += 1

	conn.commit()
	cur.close()
	conn.close()
	return inserted


def search_similar(query: str, top_k: int = 3, source: str | None = None):
	conn = get_connection()
	cur = conn.cursor()

	query_embedding = get_embedding(query)

	if source:
		cur.execute(
			"""
			SELECT content, embedding <-> %s::vector AS distance
			FROM documents
			WHERE source = %s
			ORDER BY distance
			LIMIT %s
			""",
			(to_pgvector(query_embedding), source, top_k),
		)
	else:
		cur.execute(
			"""
			SELECT content, embedding <-> %s::vector AS distance
			FROM documents
			ORDER BY distance
			LIMIT %s
			""",
			(to_pgvector(query_embedding), top_k),
		)

	rows = cur.fetchall()
	cur.close()
	conn.close()
	return rows
