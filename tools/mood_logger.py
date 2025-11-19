import datetime
import os
from tinydb import TinyDB, Query
from google.adk.tools import FunctionTool
from google.adk.tools.tool_context import ToolContext

# --- 1. Setup Database Path ---
# This ensures the JSON file is created in the ROOT folder, not inside /tools
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DB_PATH = os.path.join(BASE_DIR, 'user_memory.json')

# --- 2. Initialize Database ---
db = TinyDB(DB_PATH, indent=4, separators=(',', ': '))
mood_table = db.table('mood_history')

# --- 3. Define the Tool Function ---
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
        
    print(f"--- 💾 Memory Saved: '{mood}' to {DB_PATH} ---")
    return f"Mood saved: {mood}"

# --- 4. Export the Tool ---
# The agent will import this variable
mood_tool = FunctionTool(save_mood_to_state)