from qdrant_client.models import PointStruct
from app.db import client, COLLECTION_NAME
from app.embedder import get_embeddings
from app.schemas import DocumentIn


DEFAULT_DOCUMENTS = [
    DocumentIn(id=1, text="Machine learning basics", category="AI"),
    DocumentIn(id=2, text="Deep learning neural networks", category="AI"),
    DocumentIn(id=3, text="Healthy eating habits", category="Health"),
]


def _build_payload(doc: DocumentIn) -> dict:
    payload = {"text": doc.text, "category": doc.category}
    payload.update(doc.metadata)
    return payload


def ingest_data(documents: list[DocumentIn] | None = None) -> int:
    docs = documents if documents is not None else DEFAULT_DOCUMENTS
    vectors = get_embeddings([doc.text for doc in docs])
    points = []

    for doc, vector in zip(docs, vectors, strict=True):
        points.append(
            PointStruct(
                id=doc.id,
                vector=vector,
                payload=_build_payload(doc),
            )
        )

    client.upsert(collection_name=COLLECTION_NAME, points=points)
    return len(points)