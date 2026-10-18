import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(api_key=os.getenv("LLM_API_KEY"))

response = client.models.generate_content(
    model="gemini-3.8-flash",
    contents="Say hello to a B.Tech student in one friendly sentence.",
)
print(response.text)