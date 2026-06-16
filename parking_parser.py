import requests
import pandas as pd
import time

API_KEY = "08f22140-e0a0-4a85-8d1b-6285d3cb4cb8"
REGION_ID = 67

url = "https://catalog.api.2gis.com/3.0/items"

# Different search terms to get more parking records
queries = [
    "парковка",
    "автостоянка",
    "parking",
    "подземная парковка",
    "платная парковка"
]

all_data = []

# Loop through each search query
for query in queries:
    print(f"\nSearching for: {query}")

    page = 1

    # Demo API only allows pages 1–5
    while page <= 5:
        params = {
            "q": query,
            "region_id": REGION_ID,
            "page": page,
            "page_size": 10,
            "fields": "items.point,items.schedule",
            "key": API_KEY
        }

        response = requests.get(url, params=params)
        data = response.json()

        # Check for API errors
        if data.get("meta", {}).get("code") != 200:
            print("API Error:")
            print(data)
            break

        items = data.get("result", {}).get("items", [])

        if not items:
            print("No more items.")
            break

        print(f"Page {page}: {len(items)} records")

        for item in items:
            point = item.get("point", {})

            all_data.append({
                "id": item.get("id"),
                "name": item.get("name"),
                "address": item.get("address_name"),
                "latitude": point.get("lat"),
                "longitude": point.get("lon"),
                "link_2gis": f"https://2gis.kz/almaty/firm/{item.get('id')}",
                "working_hours": item.get("schedule", {}).get("text"),
                "tariff": "Не указано",
                "spaces": "Не указано",
                "paid_free": "Не указано"
            })

        page += 1
        time.sleep(0.3)

# Create DataFrame
df = pd.DataFrame(all_data)

print("\nBefore deduplication:", len(df))

# Remove duplicates using 2GIS ID
df.drop_duplicates(subset=["id"], inplace=True)

print("After deduplication:", len(df))

# Save to CSV
df.to_csv("almaty_parking.csv", index=False, encoding="utf-8-sig")
import os

print("\nDone!")
print("Current working directory:", os.getcwd())
print("CSV saved to:", os.path.abspath("almaty_parking.csv"))