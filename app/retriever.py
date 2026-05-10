import json

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    catalog = json.load(f)


def search_assessments(query, top_k=5):
    query = query.lower()

    scored = []

    for item in catalog:
        text = (
            item.get("name", "") + " " +
            item.get("description", "") + " " +
            " ".join(item.get("keys", []))
        ).lower()

        score = 0

        for word in query.split():
            if word in text:
                score += 1

        scored.append((score, item))

    scored.sort(key=lambda x: x[0], reverse=True)

    results = []

    for score, item in scored[:top_k]:
        results.append({
            "name": item.get("name"),
            "url": item.get("link"),
            "remote": item.get("remote"),
            "adaptive": item.get("adaptive"),
            "duration": item.get("duration"),
            "assessment_types": item.get("keys", [])
        })

    return results