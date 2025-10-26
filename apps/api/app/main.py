"""Main FastAPI application"""

import time
from contextlib import asynccontextmanager
from datetime import datetime
from typing import AsyncIterator

import sentry_sdk
from fastapi import FastAPI, HTTPException, Request, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from opentelemetry import trace
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk.trace import TracerProvider

from . import __version__
from .config import settings
from .llm_engine import llm_engine
from .models import (
    GenerateRequest,
    GenerateResponse,
    HealthResponse,
    InterpretRequest,
    InterpretResponse,
)
from .rate_limiter import rate_limiter


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncIterator[None]:
    """Lifecycle manager for startup/shutdown"""
    # Startup: Initialize observability
    if settings.sentry_dsn:
        sentry_sdk.init(
            dsn=settings.sentry_dsn,
            environment=settings.environment,
            traces_sample_rate=0.1,
        )

    if settings.otel_exporter_otlp_endpoint:
        trace.set_tracer_provider(TracerProvider())

    yield

    # Shutdown: cleanup if needed


# Create FastAPI app
app = FastAPI(
    title=settings.api_title,
    version=settings.api_version,
    description=settings.api_description,
    lifespan=lifespan,
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://sorry.monster", "https://oops.ninja", "http://localhost:*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "OPTIONS"],
    allow_headers=["*"],
)

# Add request timing middleware
@app.middleware("http")
async def add_process_time_header(request: Request, call_next: Any) -> Any:
    """Add X-Process-Time header to responses"""
    start_time = time.time()
    response = await call_next(request)
    process_time = time.time() - start_time
    response.headers["X-Process-Time"] = str(process_time)
    return response


# Instrument with OpenTelemetry
if settings.otel_exporter_otlp_endpoint:
    FastAPIInstrumentor.instrument_app(app)


@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception) -> JSONResponse:
    """Global exception handler"""
    if settings.sentry_dsn:
        sentry_sdk.capture_exception(exc)

    return JSONResponse(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        content={"error": "Internal server error", "detail": str(exc)},
    )


@app.get("/", response_model=HealthResponse)
async def root() -> HealthResponse:
    """Root endpoint - health check"""
    return HealthResponse(
        status="healthy", version=__version__, timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.get("/health", response_model=HealthResponse)
async def health() -> HealthResponse:
    """Health check endpoint"""
    return HealthResponse(
        status="healthy", version=__version__, timestamp=datetime.utcnow().isoformat() + "Z"
    )


@app.post("/v1/interpret", response_model=InterpretResponse)
async def interpret(request: Request, body: InterpretRequest) -> InterpretResponse:
    """Interpret messy incident input into structured record

    This endpoint parses raw incident descriptions, tweets, links, etc.
    into a structured incident record ready for apology generation.
    """
    # Rate limiting
    client_id = request.headers.get("X-Client-ID", request.client.host if request.client else "unknown")
    is_authed = request.headers.get("Authorization") is not None

    if not await rate_limiter.check_rate_limit(client_id, is_authed):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )

    try:
        result = await llm_engine.interpret(body)
        return result
    except Exception as e:
        if settings.sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Interpretation failed: {str(e)}",
        )


@app.post("/v1/generate", response_model=GenerateResponse)
async def generate(request: Request, body: GenerateRequest) -> GenerateResponse:
    """Generate apology drafts with guardrails applied

    This endpoint takes a structured incident record and generates
    both useful and pointless apology variants for each requested channel.
    """
    # Rate limiting
    client_id = request.headers.get("X-Client-ID", request.client.host if request.client else "unknown")
    is_authed = request.headers.get("Authorization") is not None

    if not await rate_limiter.check_rate_limit(client_id, is_authed):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )

    try:
        result = await llm_engine.generate(body)
        return result
    except Exception as e:
        if settings.sentry_dsn:
            sentry_sdk.capture_exception(e)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Generation failed: {str(e)}",
        )


@app.post("/v1/moderate")
async def moderate(request: Request, body: dict[str, Any]) -> dict[str, Any]:
    """Content moderation endpoint

    Refuse hate/violence/illegal apology requests.
    No tragedy exploitation.
    No medical/financial advice beyond boilerplate.
    """
    # Rate limiting
    client_id = request.headers.get("X-Client-ID", request.client.host if request.client else "unknown")
    is_authed = request.headers.get("Authorization") is not None

    if not await rate_limiter.check_rate_limit(client_id, is_authed):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail="Rate limit exceeded. Please try again later.",
        )

    text = body.get("text", "")

    # Basic content moderation rules
    forbidden_patterns = [
        r"\b(hate|violence|illegal|exploit)\b",
        r"\b(medical advice|financial advice)\b",
        r"\b(tragedy|disaster) (exploitation|profit)\b",
    ]

    for pattern in forbidden_patterns:
        if re.search(pattern, text.lower()):
            return {
                "allowed": False,
                "reason": "Content violates moderation policy",
                "category": "policy_violation",
            }

    return {"allowed": True, "reason": "Content passes moderation", "category": "safe"}


# Import typing for Any
from typing import Any
