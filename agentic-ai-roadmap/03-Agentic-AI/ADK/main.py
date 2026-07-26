import os
import uvicorn
from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import RedirectResponse
from pydantic import BaseModel
from typing import List

# Import social_agent methods
import social_agent

app = FastAPI(title="Antigravity GEO Copywriting Agent")

# Mount static folder for UI assets
static_path = os.path.join(os.path.dirname(__file__), "static")
os.makedirs(static_path, exist_ok=True)
app.mount("/static", StaticFiles(directory=static_path, html=True), name="static")

class GenerateRequest(BaseModel):
    trend: str
    brand_name: str
    keywords: List[str]
    audience: str

@app.get("/")
def read_root():
    return RedirectResponse(url="/static/index.html")

@app.get("/health")
def health_check():
    return {"status": "healthy", "service": "Antigravity Multi-Agent Hub"}

@app.get("/api/trends")
async def get_trends():
    try:
        trends = await social_agent.run_trend_analysis()
        return {"trends": trends}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/generate")
async def generate_copy(payload: GenerateRequest):
    try:
        result = await social_agent.generate_social_content(
            trend=payload.trend,
            brand_name=payload.brand_name,
            keywords=payload.keywords,
            audience=payload.audience
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8080))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
