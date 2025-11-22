from google.adk.agents import LlmAgent
from tools.mood_logger_tool import mood_tool 

# --- Emotion Checker Agent --- 
emotion_checker_agent = LlmAgent(
    model="gemini-2.5-flash-lite",
    name="EmotionCheckerAgent",
    description="Analyzes user text for emotion, stress, and burnout.",
    instruction="""
    You are an empathetic emotion classifier. 
    Analyze the user's text. First, classify their mood (e.g., 'tired', 'stressed', 'focused', 'neutral').
    Second, estimate a burnout score from 1-10 (1=low, 10=high).
    
    Step 1: Call the `save_mood_to_state` tool with your findings.
    Step 2: AFTER the tool finishes, you MUST respond with a distinct confirmation phrase, such as "Mood successfully logged."
    
    This confirmation is required for the system to proceed.
    """,
    # We simply list the imported tool here
    tools=[mood_tool]
)

# --- CRITICAL: Expose the agent as 'root_agent' for ADK Web ---
#root_agent = emotion_checker_agent