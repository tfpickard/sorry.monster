"""oops.ninja - Minimal instant mode apology service"""

import os
from typing import Any

import httpx
from fastapi import FastAPI, Form, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

app = FastAPI(
    title="oops.ninja",
    version="1.0.0",
    description="Instant apology generation - I'm Feeling Lucky mode",
)

templates = Jinja2Templates(directory="templates")

# API backend URL
API_URL = os.getenv("API_URL", "http://sorry_api:8083")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> Any:
    """Landing page with minimal form"""
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/lucky")
async def lucky(
    summary: str = Form(...),
    what: str = Form(...),
    harm: str = Form(...),
    severity: str = Form(default="medium"),
) -> dict[str, Any]:
    """I'm Feeling Lucky - instant apology generation

    Calls the /v1/lucky API endpoint with minimal input.
    Returns twitter and customer_email drafts only.
    """
    # Build minimal request payload
    payload = {
        "summary": summary,
        "what": what,
        "harm": harm,
        "severity": severity,
    }

    # Call /v1/lucky API endpoint
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(f"{API_URL}/v1/lucky", json=payload, timeout=60.0)
            response.raise_for_status()
            return response.json()
    except httpx.HTTPError as e:
        raise HTTPException(status_code=500, detail=f"API error: {str(e)}")


@app.get("/health")
async def health() -> dict[str, str]:
    """Health check"""
    return {"status": "healthy", "service": "oops.ninja"}
