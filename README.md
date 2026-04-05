This repository demonstrates the end-to-end journey of building vector-based AI systems, starting from fundamental similarity search to production-ready scalable architectures.

It is structured into three progressively advanced projects:

🔹 Project 1: Semantic Search (Foundations)
- Built using MiniLM local embeddings
- Implements cosine similarity manually using NumPy
- No vector database or frameworks
- Focus: understanding how embeddings and similarity search work

🔹 Project 2: RAG System with pgvector
- Stores embeddings in PostgreSQL using pgvector
- Implements document chunking and retrieval
- Integrates Gemini API for answer generation
- Includes metadata filtering and retrieval pipeline
- Focus: real-world retrieval-augmented generation (RAG)

🔹 Project 3: Scalable Vector Search System
- Built using Qdrant with HNSW indexing
- FastAPI-based API layer for querying
- Supports filtering, ANN search, and tuning
- Demonstrates production-level architecture and performance considerations
- Focus: scalability, latency, and system design

🚀 Tech Stack:
- Python
- sentence-transformers (MiniLM)
- PostgreSQL (pgvector)
- Qdrant
- FastAPI
- Gemini API

🎯 Key Learnings:
- Embeddings and vector similarity
- Approximate nearest neighbor (ANN) search
- Hybrid search and filtering
- RAG system design
- Production scaling and performance tradeoffs

This project is designed to build a deep understanding of vector databases and modern AI retrieval systems beyond high-level abstractions.
