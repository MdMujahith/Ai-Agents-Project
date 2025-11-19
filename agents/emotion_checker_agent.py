import datetime
from google.adk.agents import LlmAgent
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext
from tinydb import TinyDB, Query

# --- Long-term Database ---
  
db = TinyDB('user_memory.json')
mood_table = db.table('mood_history')

# ---Mood Saving Tool ---
def save_mood_to_state(tool_context: ToolContext, mood: str, burnout_score: int):
    """Saves the user's detected mood and burnout score to session and long-term memory."""
    
    today_str = str(datetime.date.today())
    print(f"\n--- 💡 TOOL CALLED: save_mood_to_state(mood={mood}, score={burnout_score}) ---")
    
    # --- Write to SHORT-TERM memory (for this session) ---
    tool_context.state["current_mood"] = mood 
    
    # --- Write to LONG-TERM memory (the "Digital Twin" DB) ---
    Mood = Query()
    existing = mood_table.search(Mood.date == today_str)
    
    if existing:
        mood_table.update(
            {'mood': mood, 'burnout_score': burnout_score}, 
            Mood.date == today_str
        )
    else:
        mood_table.insert({
            'date': today_str, 
            'mood': mood, 
            'burnout_score': burnout_score
        })
        
    print(f"--- 💾 Memory Saved: '{mood}' to user_memory.json ---")
    return f"Mood saved: {mood}"

# Wrap the function in the ADK's FunctionTool
mood_tool = FunctionTool(
    fn=save_mood_to_state, 
    name="save_mood_to_state", 
    description="Saves the user's mood and burnout score to memory."
)

# --- Emotion Checker Agent --- 
emotion_checker_agent = LlmAgent(
    model="gemini-1.5-flash",
    name="EmotionCheckerAgent",
    description="Analyzes user text for emotion, stress, and burnout.",
    instruction="""
    You are an empathetic emotion classifier. 
    Analyze the user's text. First, classify their mood (e.g., 'tired', 'stressed', 'focused', 'neutral').
    Second, estimate a burnout score from 1-10 (1=low, 10=high).
    You MUST call the `save_mood_to_state` tool with your findings.
    Do NOT respond to the user, just call the tool.
    """,
    tools=[mood_tool]
)
root_agent = emotion_checker_agent