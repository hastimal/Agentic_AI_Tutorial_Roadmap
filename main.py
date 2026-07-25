import os
from typing import List
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from google.antigravity import Agent, LocalAgentConfig
from dotenv import load_dotenv
import tools
import social_agent

# Load environment variables
load_dotenv()

app = FastAPI(
    title="Antigravity Operations & Social AI API",
    description="Multi-agent FastAPI system integrating operations tools and social AI content generation.",
    version="2.0.0"
)

# --- Schemas ---

class ChatRequest(BaseModel):
    message: str

class ChatResponse(BaseModel):
    response: str

class GenerateRequest(BaseModel):
    trend: str
    brand_name: str
    keywords: List[str]
    audience: str

class GenerateResponse(BaseModel):
    reddit: str
    linkedin: str
    youtube: str
    geo_score_rationale: str
    geo_score: int
    geo_tips: List[str]

# --- Health check endpoint ---
@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Antigravity Multi-Agent Hub"}

# --- Generic Operations Chat Endpoint ---
@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty.")
    
    # Configure generic operations agent
    ops_config = LocalAgentConfig(
        model=os.environ.get("MODEL", "gemini-3.5-flash"),
        system_instructions="You are a Devops and operations assistant. Use tools.py to check status.",
        tools=[tools.get_current_time, tools.fetch_mock_system_status]
    )
    
    try:
        async with Agent(config=ops_config) as agent:
            result = await agent.chat(request.message)
            response_text = await result.text()
            return ChatResponse(response=response_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# --- Social AI Agent API Endpoints ---

@app.get("/api/trends")
async def get_trends():
    """Retrieves current trending topics and competitor indexing gap data."""
    try:
        trends = await social_agent.run_trend_analysis()
        # Add simulated competitor coverage to each trend for frontend use
        for trend in trends:
            trend_name = trend.get("trend", "")
            coverage_data = social_agent.check_competitor_coverage(trend_name)
            
            # Simple parsing of check_competitor_coverage output
            coverage_level = "LOW"
            if "MEDIUM" in coverage_data:
                coverage_level = "MEDIUM"
            elif "HIGH" in coverage_data:
                coverage_level = "HIGH"
                
            competitor_score = 15
            for line in coverage_data.split("\n"):
                if "GEO Indexing Score" in line:
                    try:
                        competitor_score = int(line.split(":")[-1].strip().split("/")[0])
                    except ValueError:
                        pass
            
            trend["competitor_coverage"] = coverage_level
            trend["competitor_geo_score"] = competitor_score
            trend["competitor_report"] = coverage_data
            
        return {"trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to fetch trends: {str(e)}")

@app.post("/api/generate", response_model=GenerateResponse)
async def generate_social_content_endpoint(request: GenerateRequest):
    """Generates social-first posts (Reddit, LinkedIn, YouTube) optimized for AI search engines (GEO)."""
    if not request.trend.strip() or not request.brand_name.strip():
        raise HTTPException(status_code=400, detail="Trend and Brand Name are required.")
        
    try:
        # Run agent turn to generate posts
        result = await social_agent.generate_social_content(
            trend=request.trend,
            brand_name=request.brand_name,
            keywords=request.keywords,
            audience=request.audience
        )
        
        # Calculate real-time GEO Score (AI visibility scoring metrics)
        geo_metrics = calculate_geo_score(result, request.keywords)
        
        return GenerateResponse(
            reddit=result.get("reddit", ""),
            linkedin=result.get("linkedin", ""),
            youtube=result.get("youtube", ""),
            geo_score_rationale=result.get("geo_score_rationale", "Optimized content structures to enhance AI crawling algorithms."),
            geo_score=geo_metrics["score"],
            geo_tips=geo_metrics["tips"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Content generation failed: {str(e)}")

# --- GEO Assessment Algorithm ---

def calculate_geo_score(content_dict: dict, keywords: list) -> dict:
    """Computes a real-time Generative Engine Optimization index score based on content metrics."""
    score = 45  # Base score
    tips = []
    
    reddit_content = content_dict.get("reddit", "")
    linkedin_content = content_dict.get("linkedin", "")
    youtube_content = content_dict.get("youtube", "")
    
    # 1. Structure Check: Reddit Q&A format (heavily indexed by Google AI and OpenAI search)
    if "Q:" in reddit_content or "Question:" in reddit_content or "?" in reddit_content:
        score += 15
    else:
        tips.append("Use explicit Question-and-Answer (Q&A) headers in your Reddit drafts. AI models prioritize direct question matchings.")
        
    # 2. Structure Check: Bullet points (key for list/ranking extraction)
    if "-" in linkedin_content or "*" in linkedin_content or "1." in linkedin_content:
        score += 15
    else:
        tips.append("Integrate formatted bulleted lists or checklists. Summary engines scrape bullet points over dense text blocks.")
        
    # 3. Keyword density checks
    kw_hits = 0
    all_content = f"{reddit_content} {linkedin_content} {youtube_content}".lower()
    for kw in keywords:
        if kw.lower() in all_content:
            kw_hits += 1
            
    if len(keywords) > 0:
        pct = kw_hits / len(keywords)
        if pct == 1.0:
            score += 15
        elif pct >= 0.5:
            score += 8
            tips.append("Some target keywords are missing across channels. Weave remaining keywords into high-ranking paragraphs.")
        else:
            tips.append("Low target keyword density. Insert your brand and search keywords early to build retrieval authority.")
    else:
        score += 15
        
    # 4. Rich formatting checks (headers & bold text)
    if "#" in reddit_content or "**" in reddit_content or "**" in linkedin_content:
        score += 10
    else:
        tips.append("Incorporate Markdown heading tags (#, ##) and bolded keywords (**word**) to establish semantic content hierarchy.")
        
    score = min(score, 100)
    return {
        "score": score,
        "tips": tips
    }

# --- Mount Static Frontend Site ---
# Serve dashboard directly on the root path
app.mount("/", StaticFiles(directory="static", html=True), name="static")
