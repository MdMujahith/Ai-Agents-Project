from google.adk.agents import LlmAgent

study_planner_agent = LlmAgent(
    model="gemini-2.5-flash",
    name="StudyPlannerAgent",
    description="Creates study plans.",
    instruction="Create a study plan based on context. Adapt to mood.",
)