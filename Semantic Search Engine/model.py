from sentence_transformers import SentenceTransformer

def load_model():
    return SentenceTransformer('all-MiniLM-L6-v2')

def encode_text(model, texts):
    return model.encode(texts)