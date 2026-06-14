# utils/search.py
import json
import faiss
import streamlit as st
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH    = "embeddings/faiss_index.bin"
METADATA_PATH = "embeddings/metadata.json"
SCHEMES_PATH  = "data/schemes.json"

@st.cache_resource
def _load_search_engine():
    print("⏳ Loading search engine...")
    model = SentenceTransformer("google/muril-base-cased")
    index = faiss.read_index(INDEX_PATH)
    with open(METADATA_PATH, encoding="utf-8") as f:
        metadata = json.load(f)
    with open(SCHEMES_PATH, encoding="utf-8") as f:
        schemes = {s["id"]: s for s in json.load(f)}
    print("✅ Search engine ready")
    return model, index, metadata, schemes

def search_schemes(query: str, top_k: int = 5) -> list:
    model, index, metadata, schemes = _load_search_engine()

    query_vec = model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)
    scores, indices = index.search(query_vec, k=top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        meta = metadata[idx]
        full = schemes.get(meta["id"], {})
        results.append({
            "title":       full.get("title", ""),
            "ministry":    full.get("ministry", ""),
            "state":       full.get("state", ""),
            "description": full.get("description", ""),
            "eligibility": full.get("eligibility", ""),
            "benefits":    full.get("benefits", ""),
            "tags":        full.get("tags", []),
            "url":         full.get("url", ""),
            "score":       round(float(score), 3)
        })
    return results