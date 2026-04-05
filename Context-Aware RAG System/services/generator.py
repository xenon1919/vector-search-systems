# services/generator.py
import google.generativeai as genai
from config import settings

model = None


def _get_model():
    global model

    if model is not None:
        return model

    if not settings.gemini_api_key.strip():
        raise ValueError("GEMINI_API_KEY is not set. Add it to your .env file.")

    genai.configure(api_key=settings.gemini_api_key)
    model = genai.GenerativeModel(settings.gemini_model)
    return model

def generate_answer(query, context_docs):
    if not context_docs:
        return "Not enough information"

    context = "\n".join([doc[0] for doc in context_docs])

    prompt = f"""
    You are a helpful AI assistant.

    Use ONLY the context below to answer.
    If not found, answer exactly: Not enough information

    Context:
    {context}

    Question:
    {query}

    Answer:
    """

    response = _get_model().generate_content(prompt)
    return (response.text or "").strip() or "Not enough information"