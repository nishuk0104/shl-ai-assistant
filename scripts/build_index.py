import json
import faiss
import numpy as np
import pickle

from sentence_transformers import SentenceTransformer

# Load embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Load SHL catalog
with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    assessments = json.load(f)

documents = []
metadata = []

for item in assessments:

    text = f"""
    Name: {item.get('name', '')}

    Description:
    {item.get('description', '')}

    Job Levels:
    {', '.join(item.get('job_levels', []))}

    Assessment Types:
    {', '.join(item.get('keys', []))}

    Remote Testing:
    {item.get('remote', '')}

    Adaptive:
    {item.get('adaptive', '')}
    """

    documents.append(text)

    metadata.append({
        "name": item.get("name"),
        "url": item.get("link"),
        "description": item.get("description"),
        "job_levels": item.get("job_levels"),
        "assessment_types": item.get("keys")
    })

print("Creating embeddings...")

embeddings = model.encode(documents)

dimension = embeddings.shape[1]

index = faiss.IndexFlatL2(dimension)

index.add(np.array(embeddings).astype("float32"))

# Save FAISS index
faiss.write_index(
    index,
    "data/faiss_index/shl.index"
)

# Save metadata
with open("data/faiss_index/metadata.pkl", "wb") as f:
    pickle.dump(metadata, f)

print("FAISS index created successfully!")