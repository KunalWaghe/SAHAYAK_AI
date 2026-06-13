# utils/search.py
import json
import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# Paths
INDEX_PATH    = "embeddings/faiss_index.bin"
METADATA_PATH = "embeddings/metadata.json"
SCHEMES_PATH  = "data/schemes.json"

# Global variables — loaded once, reused every search
_model    = None
_index    = None
_metadata = None
_schemes  = None

def _load():
    global _model, _index, _metadata, _schemes
    if _model is None:
        print("⏳ Loading search engine (first time only)...")
        _model    = SentenceTransformer("google/muril-base-cased")
        _index    = faiss.read_index(INDEX_PATH)
        with open(METADATA_PATH, encoding="utf-8") as f:
            _metadata = json.load(f)
        with open(SCHEMES_PATH, encoding="utf-8") as f:
            _schemes = {s["id"]: s for s in json.load(f)}
        print("✅ Search engine ready")

def search_schemes(query: str, top_k: int = 5) -> list:
    _load()
    query_vec = _model.encode([query], convert_to_numpy=True).astype("float32")
    faiss.normalize_L2(query_vec)
    scores, indices = _index.search(query_vec, k=top_k)

    results = []
    for idx, score in zip(indices[0], scores[0]):
        meta = _metadata[idx]
        full = _schemes.get(meta["id"], {})
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