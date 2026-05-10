import json
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load FAISS index
index = faiss.read_index("data/faiss_index/shl.index")

# Load metadata
with open("data/faiss_index/metadata.pkl", "rb") as f:
    metadata = pickle.load(f)


def search_assessments(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode([query])

    # Search in FAISS index
    distances, indices = index.search(
        np.array(query_embedding).astype("float32"),
        top_k
    )

    results = []

    for idx in indices[0]:

        item = metadata[idx]

        results.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "remote": item.get("remote"),
            "adaptive": item.get("adaptive"),
            "duration": item.get("duration"),
            "description": item.get("description"),
            "assessment_types": item.get("keys", [])
        })

    return results