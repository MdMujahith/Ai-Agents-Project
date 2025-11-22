import asyncio
import os
import sys
import uuid
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv

# Try imports for different ADK versions
try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk.core.runner import Runner as InMemoryRunner

try:
    from uninav_agent.agent import uni_navigator_agent
except ImportError as e:
    print(f"❌ Agent import failed: {e}")
    sys.exit(1)


async def handle_model_event(event, runner, session_id, user_id):
    """
    Handles ALL types of streaming responses:
    - Text chunks
    - Candidate results
    - Tool calls
    - Final replies after tools
    """

    # 1️⃣ Standard text streaming (post-tool)
    if hasattr(event, "text") and event.text:
        print(event.text, end='', flush=True)

    # 2️⃣ Direct content streaming
    if hasattr(event, "content") and event.content:
        for part in event.content.parts:
            if hasattr(part, "stream_text") and part.stream_text:
                print(part.stream_text, end='', flush=True)
            elif hasattr(part, "text") and part.text:
                print(part.text, end='', flush=True)

    # 3️⃣ Candidate response + tool call detection
    candidates = getattr(event, "candidates", [])
    for candidate in candidates:
        parts = getattr(candidate.content, "parts", [])

        for part in parts:

            # Normal text responses
            if hasattr(part, "text") and part.text:
                print(part.text, end='', flush=True)

            # Tool calls when LLM decides to use a function
            if hasattr(part, "function_call") and part.function_call:
                fn = part.function_call

                print(f"\n\n--- 🔧 TOOL CALL: {fn.name} ---")
                print(f"Args: {fn.args}")

                try:
                    # Execute tool
                    tool_result = await runner.tool_service.call(
                        session_id=session_id,
                        user_id=user_id,
                        name=fn.name,
                        arguments=fn.args
                    )
                except Exception as e:
                    print(f"\n❌ Tool failed: {e}")
                    return

                # Send tool result back to model
                async for follow_up_event in runner.run_tool_response(
                    session_id=session_id,
                    user_id=user_id,
                    tool_response=tool_result
                ):
                    await handle_model_event(follow_up_event, runner, session_id, user_id)


async def main():
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("❌ ERROR: GEMINI_API_KEY missing in .env file.")
        return

    genai.configure(api_key=api_key)

    print("\n" + "=" * 60)
    print("🎓 UniNavigation Agent is ONLINE")
    print("💬 Type 'exit' to quit")
    print("=" * 60 + "\n")

    runner = InMemoryRunner(agent=uni_navigator_agent, app_name="agents")
    
    user_id = "user_01"
    session_id = str(uuid.uuid4())

    # Create a session
    try:
        await runner.session_service.create_session(
            app_name="agents",
            user_id=user_id,
            session_id=session_id
        )
    except Exception:
        pass

    # Chat loop
    while True:
        try:
            user_input = input("\nStudent: ").strip()

            if user_input.lower() in ["exit", "quit"]:
                print("\n👋 Goodbye!")
                break

            if not user_input:
                continue

            print("🤖 Agent: ", end="", flush=True)

            message = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_input)]
            )

            # Main streaming call
            async for event in runner.run_async(
                session_id=session_id,
                user_id=user_id,
                new_message=message
            ):
                await handle_model_event(event, runner, session_id, user_id)

            print("\n" + "-" * 60)

        except KeyboardInterrupt:
            print("\n⛔ Force Quit")
            break
        except Exception as e:
            print(f"\n❌ Runtime Error: {e}\n")


if __name__ == "__main__":
    asyncio.run(main())
