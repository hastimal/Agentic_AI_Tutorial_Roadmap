# 📚 Google Antigravity (AGY): CLI, SDK, and IDE Comprehensive Guide

Welcome to the ultimate **Google Antigravity (AGY)** study and installation guide! This document explains how to install, configure, and use the three core components of the Antigravity ecosystem: the **Command Line Interface (CLI)**, the **Python Software Development Kit (SDK)**, and the **Desktop Integrated Development Environment (IDE)**.

---

## 🏛️ Pillar Architecture: The Three Pillars of AGY

The Google Antigravity SDK is designed around three main architectural concepts:

1. **`Agent`**: The main entry point. It manages configurations (model selection, custom python tools, safety policies) and controls the session lifecycle.
2. **`Conversation`**: The session manager. It stores message turn history, handles context compaction, and provides streaming capabilities (like `.chat()`).
3. **`Connection`**: The underlying transport layer. It sends your prompt payload to Vertex AI or AI Studio and receives tokens. This decouples the agent logic from the backend.

---

## 💻 Step-by-Step Laptop Installation Guide

Follow these steps to set up the Antigravity SDK on your local machine:

### 1. Prerequisites
Ensure you have **Python 3.11** (or higher) installed on your machine. Check this by running:
```bash
python3 --version
```

### 2. Create a Python Virtual Environment
Navigate to your project directory and initialize a clean virtual environment:
```bash
# Create a virtual environment
python3 -m venv venv

# Activate the virtual environment
source venv/bin/activate
```

### 3. Install Package Dependencies
Install the required packages. Ensure the `google-antigravity` package is installed:
```bash
pip install google-adk google-genai dotenv
```

### 4. Configure Local Namespace and Executable Permissions
The Antigravity SDK uses a PEP 420 namespace package layout. To prevent import conflicts:
* **CRITICAL**: Never add an `__init__.py` file directly inside the root `google/` folder. This ensures other packages under `google` (like `google-genai` or cloud libraries) load correctly.
* **Harness Setup**: Enable execution permissions for the local helper binary:
  ```bash
  chmod +x google/antigravity/bin/localharness
  ```

### 5. Setup Credentials
Get your API key from [Google AI Studio](https://aistudio.google.com/app/api-keys) and write it to a `.env` file in the root of your project directory:
```env
GEMINI_API_KEY="AIzaSyYourStudioKeyHere..."
MODEL="gemini-2.5-flash"
```

---

## 🚀 1. The Antigravity CLI (`agy`)

The `agy` CLI is a command-line tool used to run agents, manage conversations, list models, and install plugins directly from your terminal.

### 📥 Installation & Setup
To install the CLI on your laptop (macOS and Linux), execute the official installation script:

```bash
# Download and install the agy CLI tool
curl -fsSL https://antigravity.google/cli/install.sh | bash

# Run the local shell path configurations setup
agy install
```

---

## 🛠️ 2. Complete `agy` Command & Flag Reference

Below is the complete reference of all flags and subcommands supported by the `agy` CLI tool:

### CLI Options (Flags)

| Flag | Description | Default / Example |
| :--- | :--- | :--- |
| `--project` | Google Cloud Project ID for the current CLI session. | `--project=gcp-10-project` |
| `--model` | Model target to use for the current CLI session. | `--model=gemini-2.5-flash` |
| `--agent` | Specific Agent to target for this CLI session. | `--agent=social_agent` |
| `--print` / `-p` | Run a single prompt non-interactively and print the response. | `-p "Tell me a joke"` |
| `--prompt-interactive` / `-i` | Run an initial prompt interactively and continue the session. | `-i "Let's begin"` |
| `--continue` / `-c` | Continue the most recent conversation session. | `-c` |
| `--conversation` | Resume a previous conversation session by its unique UUID. | `--conversation=abcd-1234` |
| `--new-project` | Initialize and create a brand-new project config for this session. | `--new-project` |
| `--mode` | Set agent execution mode for this session. Options: `accept-edits`, `plan`. | `--mode=plan` |
| `--effort` | Set reasoning effort for the current CLI session. Options: `low`, `medium`, `high`. | `--effort=high` |
| `--dangerously-skip-permissions` | Auto-approve all tool permission requests without prompting. | `--dangerously-skip-permissions` |
| `--add-dir` | Add a directory containing custom code/tools to the workspace path (repeatable). | `--add-dir=./my_tools` |
| `--sandbox` | Run in a sandbox environment with terminal command execution restrictions. | `--sandbox` |
| `--log-file` | Override the CLI execution log file destination path. | `--log-file=/tmp/run.log` |
| `--print-timeout` | Timeout duration for print mode execution wait. | `5m0s` |

### CLI Subcommands

| Subcommand | Description | Example Usage |
| :--- | :--- | :--- |
| **`models`** | Lists all available models enabled in your project context. | `agy models` |
| **`agents`** / **`agent`** | Scans the workspace and lists discovered local agent modules. | `agy agents` |
| **`changelog`** | Show changelog, notes, and release history of the CLI tool. | `agy changelog` |
| **`install`** | Configures shell environment paths, scripts, and updates system path. | `agy install` |
| **`update`** | Checks for updates and pulls the latest CLI release. | `agy update` |
| **`plugin`** / **`plugins`** | Manages local plugins (install, uninstall, list, enable, disable). | `agy plugin list` |
| **`help`** | Shows help details for standard commands or subcommands. | `agy help` |

---

## 📦 3. The Antigravity Python SDK (`google-antigravity`)

The Python SDK is the framework used to design, configure, and execute agents programmatically within your applications (e.g., in a FastAPI backend).

### 🛠️ How to Use the SDK (Basic Example)
Below is a simple script to run a local conversational agent session:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig

# 1. Define model configurations
config = LocalAgentConfig(
    model="gemini-2.5-flash",
    system_instructions="You are a polite AI guide."
)

async def main():
    # 2. Open an agent session
    async with Agent(config) as agent:
        # 3. Chat with the agent
        response = await agent.chat("Hello, Antigravity!")
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

---

## 🖥️ 4. The Antigravity Desktop IDE

The **Antigravity IDE** is a graphical desktop application tailored for agent developers to plan, execute, and monitor agent runs, view tool telemetry/cost metrics, and manage permissions interactively.

### 📥 Installation Steps
Visit the official download portal at `https://antigravity.google/download#antigravity-ide` and select the version for your operating system:

* **macOS**: 
  - Download `antigravity-ide-mac.dmg`.
  - Open the file and drag **Antigravity IDE** to your `Applications` folder.
  - *Alternative (Homebrew Cask)*:
    ```bash
    brew install --cask library/tap/antigravity-ide
    ```
* **Windows**:
  - Download `antigravity-ide-setup.exe` and follow the installation wizard.
* **Linux**:
  - Download `antigravity-ide.AppImage` or the `.deb` package.
  - Grant executable permissions:
    ```bash
    chmod +x antigravity-ide.AppImage
    ./antigravity-ide.AppImage
    ```

### 🛠️ How to Use the IDE
1. **Launch the application** on your laptop.
2. **Open Workspace**: Click *File -> Open Folder* and select your local project root (`Jangid-project`).
3. **Configure Settings**: Go to settings and add your `GEMINI_API_KEY` or select your active Google Cloud configuration.
4. **Visual Run Trace**: Select an agent module (e.g. `social_agent`) from the sidebar, type a prompt, and click **Run**. The IDE will display a visual flowchart of each step, tool execution, and thinking tokens in real-time.

---

## 🍌 5. Tutorial: Building the "Nana Banana" Stateful Inventory Agent

Let's integrate the **SDK, CLI, and IDE** by building a stateful fruit tracker agent. The agent will use `ToolContext` to remember how many **nana bananas** are currently stored in a local inventory across multiple conversation turns.

### Step 1: Create the Python Code
Create a file named `banana_agent.py` in your workspace:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig, ToolContext

# 1. Define a tool that stores state in the conversation context
def record_banana_inventory(fruit_name: str, count: int, ctx: ToolContext) -> str:
    """Updates the inventory counts for a specified fruit name.

    Args:
        fruit_name: The name of the fruit (e.g. "nana banana").
        count: The number of fruits to add.
        ctx: The tool context injected automatically by the SDK.
    """
    # Retrieve current counts dict from session state (initialize if not present)
    current_counts = ctx.get_state("banana_inventory", {})

    # Normalize name to keep matching consistent
    fruit_key = fruit_name.lower().strip()

    # Update counts
    current_counts[fruit_key] = current_counts.get(fruit_key, 0) + count
    ctx.set_state("banana_inventory", current_counts)

    total_count = current_counts[fruit_key]
    return f"Successfully added {count} {fruit_name}(s). Total count is now {total_count}."

# 2. Configure the agent settings
config = LocalAgentConfig(
    model="gemini-2.5-flash",
    tools=[record_banana_inventory],
    system_instructions=(
        "You are a helpful Fruit inventory assistant. When the user mentions adding "
        "fruits (like nana bananas or apples), always run your `record_banana_inventory` "
        "tool to log them and tell the user the updated totals."
    )
)

async def main():
    async with Agent(config) as agent:
        print("--- Turn 1 ---")
        response1 = await agent.chat("I have 5 delicious nana bananas.")
        async for chunk in response1:
            print(chunk, end="", flush=True)
        print("\n")

        print("--- Turn 2 ---")
        response2 = await agent.chat("Unload 3 more nana bananas!")
        async for chunk in response2:
            print(chunk, end="", flush=True)
        print("\n")

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 2: Test in the CLI
You can test this agent's tool calling behavior interactively from the terminal. Run `banana_agent.py` directly:
```bash
python3 banana_agent.py
```

### Step 3: Inspect inside the Antigravity IDE
1. Open the folder containing `banana_agent.py` in the **Antigravity IDE**.
2. Run a chat session from the interface.
3. Observe the **State Telemetry panel**: You can visually inspect the JSON state dictionary (`{"banana_inventory": {"nana banana": 8}}`) update in real-time as you message the agent.

---

## 🎨 6. Multimodal Image Generation: Creating a "Nana Banana" Image

To enable your Antigravity agent to generate custom images of fruits or assets (like a futuristic glowing **nana banana**!), you must register the built-in `GENERATE_IMAGE` capability inside `CapabilitiesConfig`.

### Python Sample Example: `generate_banana_image.py`

Create a new file `generate_banana_image.py` in your project folder:

```python
import asyncio
from google.antigravity import Agent, LocalAgentConfig
from google.antigravity.types import CapabilitiesConfig, BuiltinTools

# 1. Enable the built-in GENERATE_IMAGE capability tool
config = LocalAgentConfig(
    model="gemini-2.5-flash",
    system_instructions=(
        "You are a creative digital illustrator assistant. You have access to "
        f"the '{BuiltinTools.GENERATE_IMAGE.value}' tool. Whenever the user requests "
        "an image or illustration of a banana (or any object), use this tool to create it."
    ),
    capabilities=CapabilitiesConfig(
        enabled_tools=[BuiltinTools.GENERATE_IMAGE]
    ),
)

async def main():
    async with Agent(config) as agent:
        print("Sending request to generate image...")
        
        # 2. Command the agent to create the image
        response = await agent.chat(
            "Generate an image of a futuristic, glowing neon nana banana floating in deep space."
        )
        
        # Print the model's text response (which contains references to the created image artifact)
        print(await response.text())

if __name__ == "__main__":
    asyncio.run(main())
```

### Running and Verifying
1. Run the script:
   ```bash
   python3 generate_banana_image.py
   ```
2. The agent will invoke the image generation backend, output the response text, and write the generated image file into your local brain artifacts directory:
   `~/.gemini/antigravity/brain/<session_id>/artifacts/`
3. If running inside the **Antigravity IDE**, the generated image will render inline directly in your chat conversation log.
