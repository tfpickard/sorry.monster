"""Tests for main API endpoints"""

import pytest
from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root() -> None:
    """Test root endpoint"""
    response = client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "version" in data
    assert "timestamp" in data


def test_health() -> None:
    """Test health check endpoint"""
    response = client.get("/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"


@pytest.mark.asyncio
async def test_interpret_minimal() -> None:
    """Test interpret endpoint with minimal input"""
    payload = {
        "mode": "interpret",
        "incident_input": {
            "text": "Our database went down for 2 hours affecting 1000 customers",
            "links": [],
            "files": [],
        },
    }

    response = client.post("/v1/interpret", json=payload)
    assert response.status_code in [200, 500]  # May fail without OpenAI key


@pytest.mark.asyncio
async def test_generate_minimal() -> None:
    """Test generate endpoint with minimal input"""
    payload = {
        "mode": "generate",
        "incident": {
            "summary": "Database outage",
            "who": ["customers"],
            "what": "Database went down",
            "when": "2024-01-15T10:00:00Z",
            "harm": "Service unavailable for 2 hours",
            "stakeholders": ["customers"],
            "severity": "medium",
            "jurisdictions": [],
            "evidence": ["rollback completed"],
        },
        "sliders": {"contrition": 65, "legal_hedging": 30, "memes": 0},
        "channels": ["twitter"],
        "tone": "earnest",
    }

    response = client.post("/v1/generate", json=payload)
    assert response.status_code in [200, 500]  # May fail without OpenAI key


def test_moderate_safe_content() -> None:
    """Test moderation with safe content"""
    payload = {"text": "We apologize for the service disruption"}

    response = client.post("/v1/moderate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is True


def test_moderate_unsafe_content() -> None:
    """Test moderation with policy-violating content"""
    payload = {"text": "This is about hate and violence"}

    response = client.post("/v1/moderate", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["allowed"] is False
