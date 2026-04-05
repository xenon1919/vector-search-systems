# embeddings/model.py
from sentence_transformers import SentenceTransformer
from config import settings

model = SentenceTransformer(settings.embedding_model)

def get_embedding(text):
    return model.encode(text).tolist()