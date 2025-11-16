from dotenv import load_dotenv
import os

load_dotenv()

print("GROQ:", os.getenv("GROQ_API_KEY"))
print("MODEL:", os.getenv("LLM_MODEL"))
print("GITHUB_TOKEN:", os.getenv("GITHUB_TOKEN"))
