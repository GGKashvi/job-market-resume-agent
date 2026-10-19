import sys
from jobs import fetch_jobs, filter_relevant
from skills import count_skills

role = sys.argv[1] if len(sys.argv) > 1 else "backend intern"
location = sys.argv[2] if len(sys.argv) > 2 else ""

result = fetch_jobs(role, location)
if result["error"]:
    print("Error:", result["error"])
    sys.exit(1)

all_jobs = result["jobs"]
jobs = filter_relevant(all_jobs)

print(f"{len(all_jobs)} fetched, {len(jobs)} relevant after filtering "
      f"(total matching: {result['total']}) | from cache: {result['from_cache']}")

if not jobs:
    print("No relevant postings found. Try a broader search.")
    sys.exit(0)

print("\nTop skills in demand:")
for skill, n in count_skills(jobs)[:10]:
    print(f"  {skill}: {n}/{len(jobs)} jobs")

print("\nSample postings:")
for j in jobs[:5]:
    print(f"  - {j['title']} | {j['company']} | {j['location']}")
    print(f"    {j['url']}")