import json

with open("data/shl_catalog.json", "r", encoding="utf-8") as f:
    data = json.load(f)

print("TYPE:", type(data))
print("TOTAL ITEMS:", len(data))

print("\nFIRST ITEM:\n")
print(data[0])