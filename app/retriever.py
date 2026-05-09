import json
import faiss
import numpy as np

from sentence_transformers import SentenceTransformer


# Load embedding model
model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

# Load FAISS index
index = faiss.read_index(
    "data/shl_faiss.index"
)

# Load metadata
with open(
    "data/shl_metadata.json",
    "r",
    encoding="utf-8"
) as f:

    metadata = json.load(f)


def search_assessments(query, top_k=5):

    # Convert query into embedding
    query_embedding = model.encode([query])

    query_embedding = np.array(
        query_embedding,
        dtype=np.float32
    )

    # Search FAISS
    distances, indices = index.search(
        query_embedding,
        top_k
    )

    results = []

    for i in range(len(indices[0])):

        score = float(distances[0][i])

        idx = indices[0][i]

        assessment = metadata[idx]

        # Bonus ranking logic
        bonus = 0

        query_lower = query.lower()

        if (
            "java" in query_lower and
            "java" in assessment["name"].lower()
        ):
            bonus += 0.2

        if (
            "python" in query_lower and
            "python" in assessment["name"].lower()
        ):
            bonus += 0.2

        if (
            "communication" in query_lower and
            "communication" in assessment["description"].lower()
        ):
            bonus += 0.2

        final_score = score + bonus

        results.append({
            "score": final_score,
            "name": assessment["name"],
            "url": assessment["url"],
            "description": assessment["description"],
            "assessment_types": assessment["assessment_types"]
        })

    # Sort by improved score
    results = sorted(
        results,
        key=lambda x: x["score"],
        reverse=True
    )

    return results