from sentence_transformers import SentenceTransformer
import numpy as np

# Load a small model for embeddings (works within 1GB and supports CPU)
model = SentenceTransformer("all-MiniLM-L6-v2")  # ~80MB

def embed_text(text):
    """
    Returns a normalized embedding for the input text.
    """
    embedding = model.encode(text, convert_to_numpy=True, normalize_embeddings=True)
    return embedding

def embed_texts(texts):
    """
    Returns a list of normalized embeddings for multiple texts.
    """
    embeddings = model.encode(texts, convert_to_numpy=True, normalize_embeddings=True)
    return embeddings

def cosine_similarity(vec1, vec2):
    """
    Computes cosine similarity between two normalized vectors.
    """
    return np.dot(vec1, vec2)

def get_top_k_sections(query, sections, k=3):
    """
    Returns the top-k sections with highest similarity to the query.

    Parameters:
        query: string
        sections: list of section dictionaries with 'content' keys
        k: number of top matches to return

    Returns:
        List of section dicts with top similarity
    """
    section_texts = [s['content'] for s in sections]
    section_embeddings = embed_texts(section_texts)
    query_embedding = embed_text(query)

    scored_sections = []
    for section, section_emb in zip(sections, section_embeddings):
        score = cosine_similarity(query_embedding, section_emb)
        scored_sections.append((score, section))

    top_k = sorted(scored_sections, key=lambda x: x[0], reverse=True)[:k]
    return [s for _, s in top_k]
