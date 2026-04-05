# app.py
import streamlit as st
from services.retrieval import search
from services.generator import generate_answer

st.title("🧠 RAG System (pgvector + Gemini)")

query = st.text_input("Ask something:")

top_k = st.slider("Top-K Results", 1, 10, 3)

if st.button("Search"):
    if not query.strip():
        st.warning("Please enter a question before searching.")
        st.stop()

    try:
        results = search(query, top_k=top_k)
        answer = generate_answer(query, results)
    except Exception as exc:
        st.error(f"Error: {exc}")
        st.stop()

    st.subheader("Answer:")
    st.write(answer)

    st.subheader("Retrieved Context:")
    for r in results:
        st.write(r[0])