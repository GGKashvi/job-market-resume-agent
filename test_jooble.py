import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

key = os.getenv("JOOBLE_API_KEY")
url = f"https://jooble.org/api/{key}"

searches = [
    ("intern", "Bengaluru"),
    ("python intern", "Pune"),
    ("data analyst", "Mumbai"),
]

all_data = {}

for what, where in searches:
    r = requests.post(url, json={"keywords": what, "location": where}, timeout=15)
    data = r.json()
    all_data[f"{what} | {where}"] = data
    jobs = data.get("jobs", [])

    print(f"\n=== {what} | {where} ===")
    print("Status:", r.status_code, "| Total:", data.get("totalCount"), "| Returned:", len(jobs))
    for job in jobs[:5]:
        snippet = job.get("snippet", "")
        print("-", job.get("title"), "|", job.get("company"), "|", job.get("location"),
              "| snippet length:", len(snippet))

    interns = [j for j in jobs if "intern" in j.get("title", "").lower()]
    print("Titles containing 'intern':", len(interns), "of", len(jobs))

with open("sample_jooble.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2)