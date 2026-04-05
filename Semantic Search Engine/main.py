import streamlit as st
import numpy as np
import os

from model import load_model, encode_text
from utils import rank_documents
from loader import process_documents

EMBEDDINGS_FILE = "embeddings.npy"
DATA_FOLDER = "data"

st.set_page_config(page_title="Semantic Search Engine", layout="wide")

st.title("🧠 Semantic Search (MiniLM Local)")
st.write("No APIs. No LangChain. Just pure brains.")

# Load model
@st.cache_resource
def get_model():
    return load_model()

model = get_model()

# Load or create embeddings
@st.cache_data
def load_embeddings():
    documents = process_documents(DATA_FOLDER)

    if os.path.exists(EMBEDDINGS_FILE):
        embeddings = np.load(EMBEDDINGS_FILE)
    else:
        embeddings = encode_text(model, documents)
        np.save(EMBEDDINGS_FILE, embeddings)

    return documents, embeddings

documents, doc_embeddings = load_embeddings()

# UI Inputs
query = st.text_input("🔍 Enter your query")
top_k = st.slider("Top K Results", 1, 10, 3)

if query:
    query_embedding = encode_text(model, query)

    results = rank_documents(query_embedding, doc_embeddings, documents, top_k)

    st.subheader("📊 Results")

    for doc, score in results:
        st.write(f"**Score:** {score:.4f}")
        st.write(doc)
        st.markdown("---")