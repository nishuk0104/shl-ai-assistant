import json

# Load catalog
with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query, top_k=5):

    query = query.lower()

    scored_results = []

    for item in catalog:

        score = 0

        name = item.get("name", "").lower()
        description = item.get("description", "").lower()
        keys = " ".join(item.get("keys", [])).lower()

        query_words = query.split()

        for word in query_words:

            if word in name:
                score += 3

            if word in description:
                score += 2

            if word in keys:
                score += 1

        if score > 0:

            scored_results.append((score, {
                "name": item.get("name"),
                "url": item.get("link"),
                "remote": item.get("remote"),
                "adaptive": item.get("adaptive"),
                "duration": item.get("duration"),
                "description": item.get("description"),
                "assessment_types": item.get("keys", [])
            }))

    scored_results.sort(reverse=True, key=lambda x: x[0])

    return [item[1] for item in scored_results[:top_k]]