import os
import json
from dotenv import load_dotenv
from google.adk.runners import Runner
try:
    from google.adk.sessions.in_memory_session_service import InMemorySessionService as InMemoryCredentialService
except ImportError:
    from google.adk.auth.credential_service.in_memory_credential_service import InMemoryCredentialService

# Import root_agent and tools so they are exposed at the package level
from .agent import check_competitor_coverage, fetch_emerging_trends, root_agent

# Load environment variables
env_path = os.path.join(os.path.dirname(__file__), ".env")
if os.path.exists(env_path):
    load_dotenv(env_path)

# Runner setup using an in-memory session credentials service
credential_service = InMemoryCredentialService()
runner = Runner(credential_service=credential_service)

async def run_trend_analysis() -> list:
    """Fetches emerging trends using the agent's tools."""
    try:
        prompt = "Please retrieve the latest emerging trends using your fetch_emerging_trends tool."
        response_text = ""
        async for event in runner.run_async(root_agent, prompt):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text
        
        # Clean markdown code blocks from model JSON response
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("\n", 1)[0]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
            
        return json.loads(cleaned)
    except Exception as e:
        print(f"Error running trend analysis agent: {e}")
        # Fallback to direct tool call to prevent frontend crash
        return json.loads(fetch_emerging_trends())

async def generate_social_content(trend: str, brand_name: str, keywords: list, audience: str) -> dict:
    """Generates social media content for a given trend, brand, keywords, and audience."""
    try:
        prompt = (
            f"Generate optimized GEO copy for:\n"
            f"- Trend: {trend}\n"
            f"- Brand Name: {brand_name}\n"
            f"- Keywords: {', '.join(keywords)}\n"
            f"- Target Audience: {audience}\n"
            f"Be sure to check competitor coverage for this trend using your check_competitor_coverage tool first!"
        )
        response_text = ""
        async for event in runner.run_async(root_agent, prompt):
            if hasattr(event, "content") and event.content:
                for part in event.content.parts:
                    if hasattr(part, "text") and part.text:
                        response_text += part.text
                        
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            cleaned = cleaned.split("\n", 1)[-1]
        if cleaned.endswith("```"):
            cleaned = cleaned.rsplit("\n", 1)[0]
        cleaned = cleaned.strip()
        if cleaned.startswith("json"):
            cleaned = cleaned[4:].strip()
            
        return json.loads(cleaned)
    except Exception as e:
        print(f"Error generating social content: {e}")
        # Fallback to structured mock response to prevent user downtime
        return {
            "reddit": f"# Q&A: How can {brand_name} optimize for {trend}?\n\n**Q: What is {trend} and why should you care?**\n\n**A:** {trend} is changing digital media. By focusing on {', '.join(keywords)}, we can maximize engagement for {audience}.\n\n---",
            "linkedin": f"🚀 Let's talk about **{trend}**!\n\nHere are 3 key takeaways for {audience} with {brand_name}:\n\n- Takeaway 1: Focus on quality\n- Takeaway 2: Align copy structures\n- Takeaway 3: Monitor results.",
            "youtube": "[Intro Visual]\n- Welcome back! Today we are looking at how {brand_name} tackles {trend}.\n\n[Talking Points]\n- Discuss {', '.join(keywords)}\n- Target audience: {audience}\n\n[CTA]\n- Drop your comments below!",
            "geo_score_rationale": "Fallback mock content generated because the live model returned a parsing exception."
        }
