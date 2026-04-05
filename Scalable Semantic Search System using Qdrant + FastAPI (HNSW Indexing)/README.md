# Scalable Semantic Search with Qdrant + FastAPI

This repository contains a small semantic search system built with FastAPI, Qdrant, and sentence-transformer embeddings.

For a full walkthrough of the codebase, architecture, endpoints, configuration, and troubleshooting, see [docs/PROJECT_DOCUMENTATION.md](docs/PROJECT_DOCUMENTATION.md).

## Quick Start

```bash
pip install -r requirements.txt
python run.py
```

Then open:

- http://127.0.0.1:8000/
- http://127.0.0.1:8000/docs

## What it does

- Embeds text using `all-MiniLM-L6-v2`
- Stores vectors and payloads in Qdrant
- Supports semantic search with optional category filtering
- Includes a simple browser UI on the home page
- Supports local Qdrant and Qdrant Cloud through environment variables
