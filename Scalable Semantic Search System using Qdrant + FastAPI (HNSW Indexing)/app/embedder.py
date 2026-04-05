from sentence_transformers import SentenceTransformer

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text: str):
    return model.encode(text, normalize_embeddings=True).tolist()


def get_embeddings(texts: list[str]) -> list[list[float]]:
    if not texts:
        return []

    vectors = model.encode(texts, normalize_embeddings=True, show_progress_bar=False)
    return vectors.tolist()