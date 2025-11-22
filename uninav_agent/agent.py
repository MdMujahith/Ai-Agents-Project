from google.adk.agents import LlmAgent
from google.adk.tools import AgentTool

# Import sub-agents
from calender_agent.agent import calendar_agent
from emotion_checker_agent.agent import emotion_checker_agent
from planner_agent.agent import study_planner_agent

uni_navigator_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="UniNavigationAgent",
    description="Main orchestrator.",
    instruction="""
    You are the main coordinator for a student assistant.
    
    **YOUR GOLDEN RULE:**
    NEVER stop after calling a tool. You must ALWAYS respond to the user with a text summary of what the tool returned.
    
    **ROUTING LOGIC:**
    ROUTING LOGIC:
    1. **Check Mood:** Always call `EmotionCheckerAgent` first.
    2. **Chain Actions:** AFTER the mood check is complete, you MUST proceed to answer the user's actual question (e.g., checking the schedule or planning). Do not stop at the mood check.
    
    **Example Interaction:**
    User: "What is my schedule?"
    You: *Call CalendarAgent* -> *Tool returns list of exams*
    You: "I found 2 exams this week: Math on Friday and Physics on Monday." 
    (Do not just stay silent!)
    """,
    tools=[
        AgentTool(calendar_agent),
        AgentTool(emotion_checker_agent),
        AgentTool(study_planner_agent)
    ]
)
root_agent = uni_navigator_agent