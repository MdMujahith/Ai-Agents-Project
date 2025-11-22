from google.adk.tools import FunctionTool

# --- The Actual Python Function (The logic) ---
def get_calender_events(days: int = 7) -> str:
    """
    Fetches calendar events for the next N days.
    Returns a string list of events with dates and times.
    """
    
    # --- Mock Response (Fake Data for Testing) ---
    # Later, we will replace this with the real Google Calendar API code
    print(f"\n--- 🗓️ TOOL CALLED: get_calendar_events(days={days}) ---\n")
    
    mock_events = [
        "2025-11-20 10:00 AM: Data Structures Midterm",
        "2025-11-21 02:00 PM: Study Group Meeting",
        "2025-11-22 11:59 PM: Submit Assignment 3",
        "2025-11-24 09:00 AM: Football Practice"
    ]
    
    # Simulating filtering based on days (just for fun logic)
    if days < 2:
        return "\n".join(mock_events[:1]) # Only return tomorrow's event
    
    return "\n".join(mock_events)
    # --- End Mock ---

# --- The ADK Tool Definition (The Wrapper) ---
calender_tool = FunctionTool(get_calender_events)