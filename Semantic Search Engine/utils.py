import numpy as np

def cosine_similarity(a, b):
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def rank_documents(query_embedding, doc_embeddings, documents, top_k=3):
    scores = []

    for i, doc_embedding in enumerate(doc_embeddings):
        score = cosine_similarity(query_embedding, doc_embedding)
        scores.append((documents[i], score))

    scores.sort(key=lambda x: x[1], reverse=True)
    return scores[:top_k]