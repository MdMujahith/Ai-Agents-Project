import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
print(f"GEMINI_API_KEY Loaded ✅")

if not GEMINI_API_KEY:
    raise ValueError("❌ GEMINI_API_KEY Not Loaded.")