import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

from jobs import fetch_jobs, filter_relevant

load_dotenv()

client = genai.Client(api_key=os.getenv("LLM_API_KEY"))


def search_jobs(role: str, location: str = "") -> dict:
    """Search live job postings for a role, optionally in a city.

    Args:
        role: Job role to search for, for example "backend intern".
        location: Optional city or region, for example "Pune". Leave empty for all India.

    Returns:
        A dict with a list of relevant jobs (title, company, location, description, url).
    """
    print(f"[tool called: search_jobs(role={role!r}, location={location!r})]")
    result = fetch_jobs(role, location)
    if result["error"]:
        return {"error": result["error"], "jobs": []}

    jobs = filter_relevant(result["jobs"])[:10]
    return {
        "jobs": [
            {
                "title": j["title"],
                "company": j["company"],
                "location": j["location"],
                "description": j["description"],
                "url": j["url"],
            }
            for j in jobs
        ]
    }


SYSTEM = (
    "You are a career assistant for students looking for internships in India. "
    "Use the search_jobs tool to get live postings before answering. "
    "Base your answer only on the tool results. Mention which companies you saw "
    "and include the posting links. If the tool returns no jobs or an error, say so "
    "instead of guessing."
)

question = (
    "What skills are most in demand for backend internships in India right now? "
    "Search for the role 'backend intern' with no location."
)

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents=question,
    config=types.GenerateContentConfig(
        system_instruction=SYSTEM,
        tools=[search_jobs],
    ),
)

print("\n" + response.text)