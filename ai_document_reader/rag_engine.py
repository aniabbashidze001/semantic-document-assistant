from dotenv import load_dotenv
import numpy as np
import openai
import os

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")


def split_text(text, max_tokens=500):
    paragraphs = text.split("\n")
    chunks = []
    current_chunk = ""

    for para in paragraphs:
        if len(current_chunk) + len(para) < max_tokens:
            current_chunk += para + "\n"
        else:
            chunks.append(current_chunk.strip())
            current_chunk = para + "\n"

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def get_embedding(text, model="text-embedding-ada-002"):
    response = openai.Embedding.create(
        input=[text],
        model=model
    )
    return response["data"][0]["embedding"]


def process_document_for_retrieval(document_text, doc_name="Unknown Document"):
    chunks = split_text(document_text)
    embedded_chunks = []

    for chunk in chunks:
        embedding = get_embedding(chunk)
        embedded_chunks.append({
            "doc_name": doc_name,
            "chunk": chunk,
            "embedding": embedding
        })

    return embedded_chunks


def cosine_similarity(vec1, vec2):
    vec1 = np.array(vec1)
    vec2 = np.array(vec2)
    return np.dot(vec1, vec2) / (np.linalg.norm(vec1) * np.linalg.norm(vec2))


def retrieve_top_chunks(question, embedded_chunks, top_k=3, threshold=0.8):
    question_embedding = get_embedding(question)
    scored_chunks = []
    seen_chunks = set()

    for item in embedded_chunks:
        chunk_text = item["chunk"].strip()
        if chunk_text in seen_chunks:
            continue  # Skip duplicates
        score = cosine_similarity(question_embedding, item["embedding"])
        if score >= threshold:
            scored_chunks.append((score, item))
            seen_chunks.add(chunk_text)

    scored_chunks.sort(reverse=True, key=lambda x: x[0])
    top_chunks = [item for _, item in scored_chunks[:top_k]]
    return top_chunks


def generate_answer(question, top_chunks, model="gpt-3.5-turbo"):
    """
    Generate an answer using the provided top document chunks and the question.
    """
    context = "\n\n".join([chunk["chunk"] for chunk in top_chunks])

    prompt = f"""You are an AI assistant. Use only the document excerpts below to answer the question. 
If the answer is not present, say "I couldn't find that in the documents."

Document:
{context}

Question: {question}
Answer:"""

    response = openai.ChatCompletion.create(
        model=model,
        messages=[
            {"role": "user", "content": prompt}
        ],
        temperature=0.2
    )

    return response["choices"][0]["message"]["content"]

