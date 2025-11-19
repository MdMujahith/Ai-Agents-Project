import os
#import google.generativeai as genai  # Uncommented this since you use genai.configure
from dotenv import load_dotenv
from google.adk.sessions import Session  # Uncommented and fixed import of Session
from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool  # Removed any non-breaking space here

# --- 1. Import your new sub-agent ---
from agents import emotion_checker_agent

# --- 2. Load API Key ---
load_dotenv()
GEMINI_API_KEY = os.getenv("GOOGLE_API_KEY")
print(f"Loaded API key: {GEMINI_API_KEY}")  # Optional debug print
genai.configure(api_key=GEMINI_API_KEY)

# --- 3. Create a temporary Test Agent (a "mock" Main Agent) ---
test_main_agent = LlmAgent(
    model="gemini-1.5-flash",
    instruction="Your only job is to call the `EmotionCheckerAgent`.",
    tools=[
        # This wraps your sub-agent so it can be called like a tool
        AgentTool(emotion_checker_agent)
    ]
)

# --- 4. Start a Session and Test ---
print("--- Sub-Agent Test Started ---")
print("Testing if the 'test_main_agent' can call the 'EmotionCheckerAgent'...")

session = Session(agent=test_main_agent)

# This prompt should force the main agent to call the sub-agent
response = session.chat("I'm feeling really overwhelmed and tired today.")

print(f"\nAgent's Final Response: {response}")
print("\n--- Sub-Agent Test Finished ---")
print("Check for 'user_memory.json' in your folder!")
