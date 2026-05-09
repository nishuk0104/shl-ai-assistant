from app.retriever import search_assessments

query = "Java developer with communication skills"

results = search_assessments(query)

print("\nSEARCH QUERY:")
print(query)

print("\nTOP MATCHES:\n")

for i, r in enumerate(results, start=1):

    print(f"{i}. {r['name']}")
    print(f"URL: {r['url']}")
    print(f"Assessment Types: {r['assessment_types']}")
    print("-" * 50)