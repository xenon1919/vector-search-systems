import os

from dotenv import load_dotenv
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, HnswConfigDiff, SearchParams, VectorParams

load_dotenv()


def _as_bool(value: str, default: bool = False) -> bool:
    if value is None:
        return default
    return value.strip().lower() in {"1", "true", "yes", "on"}


QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
QDRANT_API_KEY = os.getenv("QDRANT_API_KEY")
QDRANT_CHECK_COMPATIBILITY = _as_bool(
    os.getenv("QDRANT_CHECK_COMPATIBILITY"), default=False
)

COLLECTION_NAME = os.getenv("QDRANT_COLLECTION", "documents")
VECTOR_SIZE = int(os.getenv("EMBEDDING_DIM", "384"))
HNSW_M = int(os.getenv("QDRANT_HNSW_M", "16"))
HNSW_EF_CONSTRUCT = int(os.getenv("QDRANT_HNSW_EF_CONSTRUCT", "100"))
SEARCH_EF = int(os.getenv("QDRANT_SEARCH_EF", "128"))

client = QdrantClient(
    url=QDRANT_URL,
    api_key=QDRANT_API_KEY,
    check_compatibility=QDRANT_CHECK_COMPATIBILITY,
)
DEFAULT_SEARCH_PARAMS = SearchParams(hnsw_ef=SEARCH_EF, exact=False)


def create_collection(force_recreate: bool = False) -> str:
    vectors_config = VectorParams(size=VECTOR_SIZE, distance=Distance.COSINE)
    hnsw_config = HnswConfigDiff(m=HNSW_M, ef_construct=HNSW_EF_CONSTRUCT)

    if force_recreate:
        client.recreate_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=vectors_config,
            hnsw_config=hnsw_config,
        )
        return "recreated"

    if not client.collection_exists(COLLECTION_NAME):
        client.create_collection(
            collection_name=COLLECTION_NAME,
            vectors_config=vectors_config,
            hnsw_config=hnsw_config,
        )
        return "created"

    return "exists"