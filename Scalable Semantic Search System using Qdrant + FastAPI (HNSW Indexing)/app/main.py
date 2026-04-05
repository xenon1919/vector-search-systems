from fastapi import FastAPI, Query
from fastapi.responses import HTMLResponse
from qdrant_client.models import FieldCondition, Filter, MatchValue

from app.db import COLLECTION_NAME, DEFAULT_SEARCH_PARAMS, client, create_collection
from app.embedder import get_embedding
from app.ingest import ingest_data
from app.schemas import IngestRequest, SearchHit, SearchRequest, SearchResponse

app = FastAPI()


@app.on_event("startup")
def on_startup() -> None:
    create_collection(force_recreate=False)


@app.get("/")
def home() -> HTMLResponse:
        html = f"""
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="utf-8" />
            <meta name="viewport" content="width=device-width, initial-scale=1" />
            <title>Semantic Search</title>
            <style>
                :root {{
                    --bg: #f4f7fb;
                    --card: #ffffff;
                    --ink: #102a43;
                    --muted: #486581;
                    --accent: #0f62fe;
                    --accent-2: #2cb1bc;
                    --border: #d9e2ec;
                }}
                * {{ box-sizing: border-box; }}
                body {{
                    margin: 0;
                    font-family: Segoe UI, -apple-system, BlinkMacSystemFont, sans-serif;
                    background: radial-gradient(circle at 20% 10%, #d9f3ff 0%, var(--bg) 45%) no-repeat;
                    color: var(--ink);
                }}
                .wrap {{
                    max-width: 900px;
                    margin: 40px auto;
                    padding: 0 16px;
                }}
                .card {{
                    background: var(--card);
                    border: 1px solid var(--border);
                    border-radius: 16px;
                    padding: 20px;
                    box-shadow: 0 8px 24px rgba(16, 42, 67, 0.08);
                }}
                h1 {{ margin: 0 0 10px; }}
                p {{ color: var(--muted); margin-top: 0; }}
                .row {{ display: grid; gap: 12px; grid-template-columns: 1fr 180px 140px; }}
                input, select, button {{
                    width: 100%;
                    padding: 10px 12px;
                    border: 1px solid var(--border);
                    border-radius: 10px;
                    font-size: 14px;
                }}
                button {{
                    background: linear-gradient(120deg, var(--accent), var(--accent-2));
                    color: #fff;
                    border: none;
                    cursor: pointer;
                }}
                .actions {{
                    margin-top: 12px;
                    display: flex;
                    gap: 10px;
                    flex-wrap: wrap;
                }}
                .actions button {{ width: auto; padding: 10px 14px; }}
                #results {{ margin-top: 18px; display: grid; gap: 10px; }}
                .item {{
                    border: 1px solid var(--border);
                    border-radius: 10px;
                    padding: 12px;
                    background: #fcfdff;
                }}
                .meta {{ color: var(--muted); font-size: 13px; margin-top: 4px; }}
                @media (max-width: 760px) {{
                    .row {{ grid-template-columns: 1fr; }}
                }}
            </style>
        </head>
        <body>
            <div class="wrap">
                <div class="card">
                    <h1>Semantic Search</h1>
                    <p>Collection: <strong>{COLLECTION_NAME}</strong></p>

                    <div class="row">
                        <input id="query" placeholder="Search text..." />
                        <input id="category" placeholder="Category (optional)" />
                        <input id="limit" type="number" min="1" max="50" value="5" />
                    </div>

                    <div class="actions">
                        <button onclick="runSearch()">Search</button>
                        <button onclick="seedData()">Seed Default Data</button>
                        <button onclick="openDocs()">Open API Docs</button>
                    </div>

                    <div id="results"></div>
                </div>
            </div>

            <script>
                async function runSearch() {{
                    const query = document.getElementById('query').value.trim();
                    const category = document.getElementById('category').value.trim();
                    const limit = Number(document.getElementById('limit').value || 5);
                    const resultsEl = document.getElementById('results');

                    if (!query) {{
                        resultsEl.innerHTML = '<div class="item">Enter a query first.</div>';
                        return;
                    }}

                    const payload = {{ query, limit }};
                    if (category) payload.category = category;

                    const res = await fetch('/search', {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json' }},
                        body: JSON.stringify(payload),
                    }});

                    if (!res.ok) {{
                        resultsEl.innerHTML = '<div class="item">Search failed. Check server logs.</div>';
                        return;
                    }}

                    const data = await res.json();
                    if (!data.results || data.results.length === 0) {{
                        resultsEl.innerHTML = '<div class="item">No results found.</div>';
                        return;
                    }}

                    resultsEl.innerHTML = data.results
                        .map(
                            (r) => `
                                <div class="item">
                                    <div><strong>${{r.text || '(no text)'}}<\/strong></div>
                                    <div class="meta">Category: ${{r.category || 'N/A'}} | Score: ${{Number(r.score).toFixed(4)}}</div>
                                </div>
                            `
                        )
                        .join('');
                }}

                async function seedData() {{
                    const resultsEl = document.getElementById('results');
                    const res = await fetch('/ingest', {{ method: 'POST' }});
                    if (!res.ok) {{
                        resultsEl.innerHTML = '<div class="item">Ingest failed.</div>';
                        return;
                    }}
                    const data = await res.json();
                    resultsEl.innerHTML = `<div class="item">Seeded ${{data.ingested}} document(s).</div>`;
                }}

                function openDocs() {{
                    window.open('/docs', '_blank');
                }}
            </script>
        </body>
        </html>
        """
        return HTMLResponse(content=html)


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "running", "collection": COLLECTION_NAME}


@app.post("/ingest")
def ingest(payload: IngestRequest | None = None) -> dict[str, int]:
    count = ingest_data(payload.documents if payload else None)
    return {"ingested": count}


def _build_filter(category: str | None) -> Filter | None:
    if not category:
        return None

    return Filter(
        must=[FieldCondition(key="category", match=MatchValue(value=category))]
    )


def _run_vector_search(query_vector: list[float], limit: int, category: str | None):
    query_filter = _build_filter(category)

    if hasattr(client, "query_points"):
        response = client.query_points(
            collection_name=COLLECTION_NAME,
            query=query_vector,
            query_filter=query_filter,
            search_params=DEFAULT_SEARCH_PARAMS,
            limit=limit,
        )
        return response.points

    if hasattr(client, "search"):
        return client.search(
            collection_name=COLLECTION_NAME,
            query_vector=query_vector,
            query_filter=query_filter,
            search_params=DEFAULT_SEARCH_PARAMS,
            limit=limit,
        )

    raise RuntimeError("Unsupported qdrant-client version: no query method found")


def _search_documents(query: str, limit: int, category: str | None) -> SearchResponse:
    vector = get_embedding(query)
    results = _run_vector_search(query_vector=vector, limit=limit, category=category)

    return SearchResponse(
        results=[
            SearchHit(
                id=result.id,
                text=result.payload.get("text", ""),
                category=result.payload.get("category"),
                score=float(result.score),
                payload=result.payload,
            )
            for result in results
        ]
    )

@app.get("/search")
def search(
    query: str = Query(..., min_length=1),
    limit: int = Query(5, ge=1, le=50),
    category: str | None = Query(default=None),
) -> SearchResponse:
    return _search_documents(query=query, limit=limit, category=category)


@app.post("/search")
def search_post(payload: SearchRequest) -> SearchResponse:
    return _search_documents(
        query=payload.query, limit=payload.limit, category=payload.category
    )