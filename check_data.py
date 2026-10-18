import json

with open("sample_responses.json", encoding="utf-8") as f:
    data = json.load(f)

for search, resp in data.items():
    jobs = resp.get("results", [])
    print(f"\n=== {search} | total: {resp.get('count')} | returned: {len(jobs)} ===")
    for job in jobs[:5]:
        desc = job.get("description", "")
        print("-", job.get("title"), "| description length:", len(desc), "| ends with:", repr(desc[-15:]))