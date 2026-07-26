# 🤖 How to Create an AI Agent Using Google ADK (Agent Development Kit)

This guide provides a step-by-step walkthrough on how to build, test, and run an autonomous AI Agent using the **Google Agent Development Kit (ADK)** Python SDK.

---

## 📋 Table of Contents
1. [Prerequisites & Environment Setup](#1-prerequisites--environment-setup)
2. [Step 1: Scaffolding a New Agent](#step-1-scaffolding-a-new-agent)
3. [Step 2: Defining Custom Tools](#step-2-defining-custom-tools)
4. [Step 3: Configuring the LLM Agent](#step-3-configuring-the-llm-agent)
5. [Step 4: Exposing Agent Package Interfaces](#step-4-exposing-agent-package-interfaces)
6. [Step 5: Testing the Agent Locally](#step-5-testing-the-agent-locally)
7. [Step 6: Programmatic Execution (FastAPI/Scripts)](#step-6-programmatic-execution-fastapiscripts)

---

## 🔌 1. Prerequisites & Environment Setup

Before starting, make sure you have Python 3.11+ installed and set up a virtual environment:

```bash
# Initialize virtual environment
python3 -m venv venv
source venv/bin/activate

# Install the Google ADK and dependency packages
pip install google-adk google-genai dotenv
```

Configure your credentials in a `.env` file in your workspace:
```env
GEMINI_API_KEY="AIzaSy..."
```

---

## 🛠️ Step 1: Scaffolding a New Agent

The ADK CLI provides a scaffolding command that sets up the required package structure for an agent. Run the following command in your terminal:

```bash
# Create agent directory structure
adk create my_agent
```

This creates a directory named `my_agent/` containing:
- `__init__.py`: Package-level entry point exposing runner execution.
- `agent.py`: Agent configurations, persona, model settings, and tool definitions.
- `.env`: Local environment configuration variables.

---

## 🔧 Step 2: Defining Custom Tools

Tools are standard Python functions that your agent can autonomously choose to run. **The docstring is the most critical part of a tool** because the LLM uses it to understand what the tool does, what parameters it accepts, and what type of data it returns.

Open `my_agent/agent.py` and define a custom tool:

```python
def fetch_weather_report(location: str) -> str:
    """Retrieves the current weather status for a specific city.

    Args:
        location: The name of the city, e.g., "London" or "Paris".
    
    Returns:
        A text description containing the current weather and temperature.
    """
    # Integrate weather APIs or databases here.
    # For demonstration, we return a mock value.
    if location.lower() == "london":
        return "Rainy, 15°C with moderate winds."
    return f"Clear skies, 22°C in {location}."
```

---

## ⚙️ Step 3: Configuring the LLM Agent

Next, configure your main agent. Import the `Agent` class from `google.adk.agents.llm_agent` and define its properties (such as its model, system instructions, and registered tools) in `my_agent/agent.py`:

```python
from google.adk.agents.llm_agent import Agent

# Define the system prompt detailing constraints and persona
system_instructions = (
    "You are a helpful travel assistant. You have access to the `fetch_weather_report` tool. "
    "Whenever a user asks about travel advice, always look up the weather for their destination "
    "first to give accurate recommendations."
)

# Instantiate the main Agent
root_agent = Agent(
    model="gemini-2.5-flash",
    name="travel_agent",
    description="A travel assistant agent with weather tools.",
    instruction=system_instructions,
    tools=[fetch_weather_report]
)
```

---

## 📦 Step 4: Exposing Agent Package Interfaces

To allow other applications (like a web server or the CLI) to load the agent cleanly, update `my_agent/__init__.py`. We set up a compatible `InMemorySessionService` and define a wrapper function:

```python
import os
from dotenv import load_dotenv
from google.adk.runners import Runner

# Handle multi-version ADK Session Service imports dynamically
try:
    from google.adk.sessions.in_memory_session_service import InMemorySessionService as InMemoryCredentialService
except ImportError:
    from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService

# Import agent objects
from .agent import fetch_weather_report, root_agent

# Load variables
load_dotenv()

# Setup Runner session
credential_service = InMemoryCredentialService()
runner = Runner(credential_service=credential_service)
```

---

## ⚡ Step 5: Testing the Agent Locally

You can test your agent interactively from the command line using the ADK CLI:

```bash
# Execute your agent in the terminal
adk run my_agent
```

### Expected Interactive Log:
```text
Running agent root_agent, type exit to exit.
[user]: What should I pack for my trip to London tomorrow?
[agent]: Let's look up the weather in London first to determine what you should pack.
[tool_call]: fetch_weather_report(location="london") -> "Rainy, 15°C with moderate winds."
[agent]: It looks like London will be rainy and cool (15°C) tomorrow. Make sure to pack an umbrella, rain jacket, and warm layers!
```

---

## 💻 Step 6: Programmatic Execution (FastAPI/Scripts)

If you want to invoke your agent programmatically inside a web service or script, run it asynchronously using the ADK `runner`:

```python
import asyncio
from my_agent import runner, root_agent

async def travel_chat():
    prompt = "I want to visit Tokyo. What is the weather like there?"
    print(f"User: {prompt}\n")
    
    # Run agent async and stream turn events
    async for event in runner.run_async(root_agent, prompt):
        if hasattr(event, "content") and event.content:
            for part in event.content.parts:
                if hasattr(part, "text") and part.text:
                    print(part.text, end="", flush=True)
    print("\n")

if __name__ == "__main__":
    asyncio.run(travel_chat())
```
