import os
import json
from typing import List, Dict, Any
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv

load_dotenv()

# --- Custom Agent Tools ---

def fetch_emerging_trends() -> str:
    """Retrieves the latest emerging trends in technology, digital marketing, and AI.
    
    Returns:
        A JSON string containing the trends list with momentum scores and targeted keywords.
    """
    trends = [
        {
            "id": 1,
            "trend": "Generative Engine Optimization (GEO)",
            "description": "Optimizing website and social media content for AI search engines like ChatGPT, Claude, and Google AI Overviews rather than traditional search engines.",
            "momentum": "94%",
            "volume_change": "+210% MoM",
            "keywords": ["GEO", "AI Search Engine Optimization", "Generative Engine Optimization", "LLM ranking factors"]
        },
        {
            "id": 2,
            "trend": "Local LLM Deployments for Enterprise",
            "description": "Enterprises transitioning away from public cloud APIs to locally-run open-weights LLMs for privacy, cost control, and latency optimization.",
            "momentum": "88%",
            "volume_change": "+145% MoM",
            "keywords": ["Local LLM", "Private AI", "Llama 3.1 enterprise", "vLLM deployment", "Self-hosted AI"]
        },
        {
            "id": 3,
            "trend": "Model Context Protocol (MCP) Integration",
            "description": "The standardized protocol developed by Anthropic allowing LLMs to seamlessly connect to local files, tools, database nodes, and cloud APIs.",
            "momentum": "92%",
            "volume_change": "+340% MoM",
            "keywords": ["MCP server", "Model Context Protocol", "LLM tool integration", "mcp sdk python"]
        },
        {
            "id": 4,
            "trend": "Social Media Crawling for AI Search",
            "description": "AI search engines heavily parsing user-generated content from Reddit, LinkedIn, and YouTube transcripts for real-time recommendations.",
            "momentum": "91%",
            "volume_change": "+180% MoM",
            "keywords": ["Reddit AI licensing", "YouTube transcript parsing", "ChatGPT real-time search", "LinkedIn indexing"]
        }
    ]
    return json.dumps(trends, indent=2)

def check_competitor_coverage(trend_name: str) -> str:
    """Checks the competitor footprint and indexing coverage for a specific emerging trend.
    
    Args:
        trend_name: The name of the trend to analyze.
    
    Returns:
        A text analysis showing competitor presence and optimization gaps.
    """
    trend_lower = trend_name.lower()
    
    if "geo" in trend_lower or "generative engine" in trend_lower:
        return (
            "--- COMPETITOR ANALYTICS FOR: GEO ---\n"
            "- Competitor Coverage Level: VERY LOW\n"
            "- Competitor Channel Footprint: 85% of competitors are publishing standard SEO blog posts. 0% are optimized for AI summaries.\n"
            "- Content Gaps: No competitors have direct Q&A blocks, structured definitions, or community-based discussions (Reddit/Quora).\n"
            "- GEO Indexing Score: 12/100 (Competitors are invisible to AI Overviews for this topic).\n"
            "- Recommendation: Publish a highly detailed, Q&A structured guide. Seed discussion threads on Reddit using keyword 'GEO ranking factors'."
        )
    elif "local llm" in trend_lower or "enterprise" in trend_lower:
        return (
            "--- COMPETITOR ANALYTICS FOR: LOCAL LLMs ---\n"
            "- Competitor Coverage Level: MEDIUM\n"
            "- Competitor Channel Footprint: High volume of cloud host comparison articles. Moderate activity on LinkedIn.\n"
            "- Content Gaps: Lack of real-world deployment walkthroughs, cost-benefit spreadsheets, or step-by-step videos.\n"
            "- GEO Indexing Score: 45/100.\n"
            "- Recommendation: Create a detailed code walkthrough or script setup, package it in GitHub, and post a LinkedIn guide showcasing cost comparisons."
        )
    elif "mcp" in trend_lower or "protocol" in trend_lower:
        return (
            "--- COMPETITOR ANALYTICS FOR: MODEL CONTEXT PROTOCOL (MCP) ---\n"
            "- Competitor Coverage Level: LOW\n"
            "- Competitor Channel Footprint: Basic news announcements. Almost no developer-level implementation guides.\n"
            "- Content Gaps: Few practical Python or Node.js MCP server code samples. Lack of tutorials explaining custom tool creation.\n"
            "- GEO Indexing Score: 18/100.\n"
            "- Recommendation: Build a simple MCP repository, publish a YouTube step-by-step video (ensure text transcripts contain full instructions), and write a Reddit post in r/LocalLLaMA."
        )
    else:
        return (
            f"--- COMPETITOR ANALYTICS FOR: '{trend_name}' ---\n"
            "- Competitor Coverage Level: HIGH\n"
            "- Competitor Channel Footprint: Competitors have saturated general blogs and social updates.\n"
            "- Content Gaps: Heavy on marketing buzzwords, extremely light on technical details and data statistics.\n"
            "- GEO Indexing Score: 70/100.\n"
            "- Recommendation: Focus on contrarian or data-backed content. Draft an opinionated piece questioning the status quo to drive organic shares."
        )

# --- Agent System Configuration ---

system_instructions = (
    "You are a Senior GEO (Generative Engine Optimization) Content Copywriter and Trend Strategist. "
    "Your objective is to identify emerging trends, find gaps in competitor content, and write social-first "
    "posts that are highly engaging for humans AND optimized for AI search engines to find, parse, and cite.\n\n"
    "When generating posts for a trend, you MUST output a JSON object containing the following keys:\n"
    "1. 'reddit': A deep, structured, community-oriented post formatted in Markdown (often structured as Q&A since LLMs crawl Q&A formatting highly).\n"
    "2. 'linkedin': A professional, punchy, thought-leadership post (using bullet points and clear takeaways).\n"
    "3. 'youtube': A clean video script with an introduction, key talking points, and call to action (structured with easy-to-read lines so YouTube automatic transcription maps it perfectly for AI crawling).\n"
    "4. 'geo_score_rationale': A brief explanation of how you optimized the content for AI search indexers (e.g. direct definitions, bolding keywords, formatting structure).\n\n"
    "Do NOT wrap the JSON inside markdown code blocks (like ```json). Respond with the raw JSON string ONLY."
)

social_agent_config = LocalAgentConfig(
    model=os.environ.get("MODEL", "gemini-3.5-flash"),
    system_instructions=system_instructions,
    tools=[fetch_emerging_trends, check_competitor_coverage]
)

async def run_trend_analysis() -> List[Dict[str, Any]]:
    """Runs trend scan using the Agent and returns the JSON output of current trends."""
    async with Agent(config=social_agent_config) as agent:
        # Ask the agent to look up trends using its tools
        response = await agent.chat("Fetch the latest emerging trends using your tools and return them as a list.")
        response_text = await response.text()
        
        try:
            # Attempt to parse as list
            # Clean possible markdown wrap just in case
            if "```" in response_text:
                response_text = response_text.split("```")[1]
                if response_text.startswith("json"):
                    response_text = response_text[4:]
            return json.loads(response_text.strip())
        except Exception:
            # Fallback direct parsing of our tool
            return json.loads(fetch_emerging_trends())

async def generate_social_content(trend: str, brand_name: str, keywords: List[str], audience: str) -> Dict[str, Any]:
    """Instructs the Antigravity Agent to analyze competitor gaps and construct social posts."""
    prompt = (
        f"Analyze competitor coverage for the trend: '{trend}'. "
        f"Then generate highly optimized social content for the brand '{brand_name}'.\n"
        f"Keywords to weave in: {', '.join(keywords)}.\n"
        f"Target audience: {audience}.\n"
        "Remember to optimize heavily for GEO (Generative Engine Optimization) based on competitor gaps, "
        "and return a raw JSON object with keys: 'reddit', 'linkedin', 'youtube', and 'geo_score_rationale' as instructed."
    )
    
    async with Agent(config=social_agent_config) as agent:
        response = await agent.chat(prompt)
        response_text = await response.text()
        
        # Clean response if wrapped in markdown
        cleaned = response_text.strip()
        if cleaned.startswith("```"):
            # strip start/end lines
            lines = cleaned.split("\n")
            if lines[0].startswith("```"):
                lines = lines[1:]
            if lines[-1].startswith("```"):
                lines = lines[:-1]
            cleaned = "\n".join(lines).strip()
            
        try:
            return json.loads(cleaned)
        except Exception as e:
            # Backup mock generator if LLM output fails parsing
            print(f"Error parsing agent JSON output: {e}. Output was: {response_text}")
            
            # Simple fallback response
            return {
                "reddit": f"# Q: How does {brand_name} solve the challenges of {trend}?\n\nHere is a detailed guide on utilizing {', '.join(keywords)} to stay ahead...",
                "linkedin": f"🚨 Emerging Trend: {trend} is changing how we work.\n\nHere is how {brand_name} is using {', '.join(keywords)} to drive success. 🧵👇",
                "youtube": f"[Intro: Energetic host talking about {trend}]\nHey everyone! Today we are looking at how {brand_name} implements {keywords[0]}...",
                "geo_score_rationale": "Optimized by embedding clear question headings (Q&A structure) for Reddit crawling, bullet points for LinkedIn summaries, and clean speech formatting for YouTube auto-generated captions."
            }
