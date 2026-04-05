# main.py
import os

from services.retrieval import search
from services.generator import generate_answer

query = os.getenv("RAG_QUERY", "What is machine learning?")

try:
	results = search(query, top_k=5)
	answer = generate_answer(query, results)

	print("\nANSWER:\n", answer)
except Exception as exc:
	print(f"RAG pipeline failed: {exc}")