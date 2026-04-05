import os

def load_text_files(folder_path):
    documents = []

    for file in os.listdir(folder_path):
        if file.endswith(".txt"):
            with open(os.path.join(folder_path, file), "r", encoding="utf-8") as f:
                documents.append(f.read())

    return documents


def chunk_text(text, chunk_size=100):
    words = text.split()
    chunks = []

    for i in range(0, len(words), chunk_size):
        chunk = " ".join(words[i:i+chunk_size])
        chunks.append(chunk)

    return chunks


def process_documents(folder_path):
    raw_docs = load_text_files(folder_path)

    all_chunks = []
    for doc in raw_docs:
        chunks = chunk_text(doc)
        all_chunks.extend(chunks)

    return all_chunks