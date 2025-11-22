import asyncio
import os
import sys
import uuid
import google.generativeai as genai
from google.genai import types
from dotenv import load_dotenv

# --- 1. Import the Runner ---
try:
    from google.adk.runners import InMemoryRunner
except ImportError:
    from google.adk.core.runner import Runner as InMemoryRunner

# --- 2. Import your Root Agent ---
try:
    from uninav_agent.agent import uni_navigator_agent
except ImportError as e:
    print(f"❌ Error importing agents: {e}")
    sys.exit(1)

async def main():
    # --- Setup ---
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("❌ Error: GEMINI_API_KEY not found.")
        return

    try:
        genai.configure(api_key=api_key)
    except Exception as e:
        print(f"❌ Error configuring API: {e}")
        return

    print("\n" + "="*50)
    print("🎓 UniNavigation Agent is ONLINE")
    print("   Type 'exit' to stop.")
    print("="*50 + "\n")

    # --- 3. Initialize Runner ---
    # Ensure app_name matches the agent's expectation ("agents")
    runner = InMemoryRunner(agent=uni_navigator_agent, app_name="agents")
    
    user_id = "user_01" 
    # FIX: Generate a session ID manually
    session_id = str(uuid.uuid4())

    # --- 4. Explicitly Create Session with known ID ---
    try:
        # We try to create the session with our explicit ID first.
        # This ensures it exists before we try to run it.
        await runner.session_service.create_session(
            app_name="agents",
            user_id=user_id,
            session_id=session_id 
        )
    except AttributeError:
        # If create_session doesn't exist or fails, we proceed.
        # Some runner versions create it lazily on the first run().
        pass
    except Exception as e:
        # If it fails for another reason (e.g. session exists), just log and continue
        # print(f"Session creation note: {e}") 
        pass

    # --- 5. The Chat Loop ---
    while True:
        try:
            user_text = input("\nStudent: ").strip()
            
            if user_text.lower() in ["exit", "quit", "bye"]:
                print("\n👋 Goodbye!")
                break
            
            if not user_text:
                continue

            print("🤖 Agent thinking...", end="\r")
            
            # Prepare the Message
            message_content = types.Content(
                role="user",
                parts=[types.Part.from_text(text=user_text)]
            )

            full_response = ""
            
            # --- 6. Run Async ---
            # We pass the explicit session_id we generated/created.
            async for event in runner.run_async(
                session_id=session_id, 
                user_id=user_id, 
                new_message=message_content
            ):
                if hasattr(event, 'text') and event.text:
                    full_response += event.text
            
            print(f"\r🤖 Agent: {full_response}\n")
            print("-" * 30)

        except KeyboardInterrupt:
            print("\nForce quit.")
            break
        except Exception as e:
            print(f"\n❌ Error: {e}\n")

if __name__ == "__main__":
    asyncio.run(main())