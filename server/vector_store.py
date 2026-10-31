from typing import Any, List

import chromadb
import requests

from config import Config
from documents import DocumentChunk

# How long (in seconds) to wait for the local model service before giving up.
REQUEST_TIMEOUT_SECONDS = 60


class ModelServiceError(Exception):
    """Raised when the local model service (Ollama) cannot be reached or fails."""


def get_chroma_client():
    """Create and return a persistent Chroma client that saves to Config.CHROMA_PATH."""
    return chromadb.PersistentClient(path=Config.CHROMA_PATH)


def get_or_create_collection():
    """
    Get (or create) the Chroma collection for the knowledge assistant.

    We use cosine distance because it measures how close two pieces of text are
    in *meaning* (the direction of their vectors), not their length.
    """
    client = get_chroma_client()
    return client.get_or_create_collection(
        name=Config.COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )


def get_embedding(text: str) -> list[float]:
    """
    Create an embedding (a list of numbers that captures meaning) for some text
    by asking the local Ollama service.
    """
    url = f"{Config.OLLAMA_BASE_URL.rstrip('/')}/api/embed"
    # Ollama's /api/embed expects the text under the key "input".
    payload = {"model": Config.EMBEDDING_MODEL, "input": text}

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT_SECONDS)
        response.raise_for_status()
        data = response.json()
    except (requests.RequestException, ValueError) as error:
        raise ModelServiceError(
            f"Could not create an embedding. Is Ollama running and is the "
            f"'{Config.EMBEDDING_MODEL}' model pulled? ({error})"
        ) from error

    # /api/embed returns {"embeddings": [[...]]}. Older Ollama versions
    # (/api/embeddings) return {"embedding": [...]}, so accept both.
    embeddings = data.get("embeddings")
    if embeddings and isinstance(embeddings[0], list) and embeddings[0]:
        return embeddings[0]
    if isinstance(data.get("embedding"), list) and data["embedding"]:
        return data["embedding"]

    raise ModelServiceError("The embedding service returned no embedding.")


def seed_vector_store(chunks: List[DocumentChunk]) -> int:
    """
    Add document chunks to the Chroma collection and return how many were stored.

    upsert() adds new chunks and updates existing ones with the same id, so
    running the seed script twice does not create duplicates.
    """
    if not chunks:
        return 0

    collection = get_or_create_collection()

    ids = [chunk.id for chunk in chunks]
    documents = [chunk.text for chunk in chunks]
    metadatas = [
        {
            "source": chunk.source,
            "title": chunk.title,
            "chunk_index": chunk.chunk_index,
        }
        for chunk in chunks
    ]
    embeddings = [get_embedding(chunk.text) for chunk in chunks]

    collection.upsert(
        ids=ids,
        documents=documents,
        metadatas=metadatas,
        embeddings=embeddings,
    )

    return len(chunks)


def retrieve_relevant_chunks(question: str, top_k: int | None = None) -> list[dict[str, Any]]:
    """
    Find the chunks whose meaning is closest to the question.

    Returns a list of dictionaries with text, source, title, chunk_index and
    distance (smaller distance = closer match).
    """
    if not question or not question.strip():
        return []

    n_results = top_k if top_k is not None else Config.TOP_K

    collection = get_or_create_collection()
    if collection.count() == 0:
        # Nothing has been seeded yet, so there is nothing to retrieve.
        return []

    query_embedding = get_embedding(question.strip())
    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=min(n_results, collection.count()),
        include=["documents", "metadatas", "distances"],
    )

    # Chroma returns one list per query; we only sent one question.
    documents = (results.get("documents") or [[]])[0]
    metadatas = (results.get("metadatas") or [[]])[0]
    distances = (results.get("distances") or [[]])[0]

    chunks = []
    for text, metadata, distance in zip(documents, metadatas, distances):
        metadata = metadata or {}
        chunks.append(
            {
                "text": text,
                "source": metadata.get("source", "unknown"),
                "title": metadata.get("title", "Unknown Source"),
                "chunk_index": metadata.get("chunk_index"),
                "distance": distance,
            }
        )

    return chunks
