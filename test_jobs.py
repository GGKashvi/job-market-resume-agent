import os
import json
import requests
from dotenv import load_dotenv

load_dotenv()

URL = "https://api.adzuna.com/v1/api/jobs/in/search/1"

searches = [
    ("python developer intern", "Bangalore"),
    ("data analyst intern", "Mumbai"),
    ("backend intern", ""),
]

all_data = {}

for what, where in searches:
    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_APP_KEY"),
        "what": what,
        "results_per_page": 20,
    }
    if where:
        params["where"] = where

    r = requests.get(URL, params=params, timeout=15)
    data = r.json()
    all_data[f"{what} | {where or 'anywhere'}"] = data

    print(f"\n=== {what} | {where or 'anywhere'} ===")
    print("Status:", r.status_code, "| Total jobs:", data.get("count"))
    for job in data.get("results", [])[:5]:
        title = job.get("title", "N/A")
        company = (job.get("company") or {}).get("display_name", "N/A")
        location = (job.get("location") or {}).get("display_name", "N/A")
        print("-", title, "|", company, "|", location)

with open("sample_responses.json", "w", encoding="utf-8") as f:
    json.dump(all_data, f, indent=2)