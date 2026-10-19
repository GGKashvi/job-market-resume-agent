import re

SKILLS = [
    "python", "java", "javascript", "typescript", "c++", "go", "sql",
    "react", "node.js", "django", "flask", "fastapi", "spring boot",
    "mysql", "postgresql", "mongodb", "redis",
    "docker", "kubernetes", "aws", "azure", "gcp", "git", "linux",
    "rest", "api", "html", "css", "machine learning", "langchain",
]


def count_skills(jobs):
    """Return [(skill, number_of_jobs_mentioning_it)], most common first."""
    counts = {}
    for job in jobs:
        text = (job["title"] + " " + job["description"]).lower()
        for skill in SKILLS:
            pattern = r"(?<![a-z0-9])" + re.escape(skill) + r"(?![a-z0-9])"
            if re.search(pattern, text):
                counts[skill] = counts.get(skill, 0) + 1
    return sorted(counts.items(), key=lambda x: x[1], reverse=True)