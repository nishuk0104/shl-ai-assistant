import requests
import json
import re

url = "https://tcp-us-prod-rnd.shl.com/voiceRater/shl-ai-hiring/shl_product_catalog.json"

response = requests.get(url)

raw_text = response.text

# Remove invalid control characters
clean_text = re.sub(r'[\x00-\x1F\x7F]', '', raw_text)

data = json.loads(clean_text)

with open("data/shl_catalog.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4)

print("Catalog downloaded and cleaned successfully!")