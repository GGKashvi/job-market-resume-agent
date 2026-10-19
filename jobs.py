import os
import json
import time
import hashlib
import requests
from dotenv import load_dotenv

load_dotenv()

CACHE_DIR = ".cache"
CACHE_TTL = 60 * 60  # 1 hour while developing; use 600 (10 min) in production

RELEVANT_WORDS = ["intern", "trainee", "fresher", "graduate", "entry level", "entry-level"]


def _cache_path(key):
    os.makedirs(CACHE_DIR, exist_ok=True)
    return os.path.join(CACHE_DIR, hashlib.md5(key.encode()).hexdigest() + ".json")


def _read_cache(key):
    path = _cache_path(key)
    if os.path.exists(path) and time.time() - os.path.getmtime(path) < CACHE_TTL:
        with open(path, encoding="utf-8") as f:
            return json.load(f)
    return None


def _write_cache(key, data):
    with open(_cache_path(key), "w", encoding="utf-8") as f:
        json.dump(data, f)


def _fetch_adzuna(role, location, limit):
    params = {
        "app_id": os.getenv("ADZUNA_APP_ID"),
        "app_key": os.getenv("ADZUNA_APP_KEY"),
        "what": role,
        "results_per_page": limit,
    }
    if location:
        params["where"] = location

    r = requests.get(
        "https://api.adzuna.com/v1/api/jobs/in/search/1", params=params, timeout=15
    )
    r.raise_for_status()
    data = r.json()

    jobs = []
    for j in data.get("results", []):
        jobs.append({
            "title": j.get("title", "N/A"),
            "company": (j.get("company") or {}).get("display_name", "N/A"),
            "location": (j.get("location") or {}).get("display_name", "N/A"),
            "description": j.get("description", ""),
            "url": j.get("redirect_url", ""),
            "source": "adzuna",
        })
    return {"jobs": jobs, "total": data.get("count", len(jobs))}


def fetch_jobs(role, location="", limit=20, source="adzuna"):
    """Fetch live jobs. Always returns a dict with the same shape."""
    key = f"{source}|{role}|{location}|{limit}"

    cached = _read_cache(key)
    if cached:
        return {**cached, "from_cache": True, "error": None}

    try:
        if source == "adzuna":
            result = _fetch_adzuna(role, location, limit)
        else:
            return {"jobs": [], "total": 0, "from_cache": False,
                    "error": f"Unknown source: {source}"}
    except requests.RequestException as e:
        return {"jobs": [], "total": 0, "from_cache": False,
                "error": f"Could not fetch jobs: {e}"}

    _write_cache(key, result)
    return {**result, "from_cache": False, "error": None}


def filter_relevant(jobs):
    """Keep only intern / trainee / fresher style roles."""
    return [j for j in jobs if any(w in j["title"].lower() for w in RELEVANT_WORDS)]