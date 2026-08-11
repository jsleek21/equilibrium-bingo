"""Seed the `items` table via Supabase's REST API. Run after schema.sql has been applied."""
import json
import urllib.request

SUPABASE_URL = "https://nmwbwclpwvbcenhxfirw.supabase.co"
API_KEY = "sb_publishable_VlC6QzuXAYyKrfF-lf8V0Q_Vh8a-k5-"

seed = json.load(open("seed.json", encoding="utf-8"))

BATCH = 15
url = f"{SUPABASE_URL}/rest/v1/items"
headers = {
    "apikey": API_KEY,
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json",
    "Prefer": "resolution=merge-duplicates",
}

for i in range(0, len(seed), BATCH):
    chunk = seed[i:i + BATCH]
    data = json.dumps(chunk).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req) as resp:
            print(f"batch {i}-{i+len(chunk)}: {resp.status}")
    except urllib.error.HTTPError as e:
        print(f"batch {i}-{i+len(chunk)}: ERROR {e.code} {e.read().decode()[:300]}")

print("done")
