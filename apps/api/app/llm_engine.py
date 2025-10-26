"""LLM Engine - Core apology generation logic with guardrails"""

import json
import re
from typing import Any

from openai import AsyncOpenAI

from .config import settings
from .models import (
    Channel,
    ChannelDraft,
    Detectors,
    GenerateRequest,
    GenerateResponse,
    Incident,
    InterpretRequest,
    InterpretResponse,
    Metrics,
    Severity,
)


class LLMEngine:
    """LLM-powered apology generation engine"""

    def __init__(self) -> None:
        self.client = AsyncOpenAI(api_key=settings.openai_api_key)
        self.model = settings.openai_model

    async def interpret(self, request: InterpretRequest) -> InterpretResponse:
        """Interpret messy incident input into structured record"""
        system_prompt = self._build_interpret_system_prompt()
        user_prompt = self._build_interpret_user_prompt(request)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.3,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")

        result = json.loads(content)
        return InterpretResponse(**result)

    async def generate(self, request: GenerateRequest) -> GenerateResponse:
        """Generate apology drafts with guardrails applied"""
        # Apply severity-based clamps
        request = self._apply_severity_clamps(request)

        # Validate strategies
        adjustments = self._validate_strategies(request)

        system_prompt = self._build_generate_system_prompt()
        user_prompt = self._build_generate_user_prompt(request)

        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.7,
            response_format={"type": "json_object"},
        )

        content = response.choices[0].message.content
        if not content:
            raise ValueError("Empty response from LLM")

        result = json.loads(content)

        # Add our adjustments to the result
        if "adjustments" not in result:
            result["adjustments"] = []
        result["adjustments"].extend(adjustments)

        return GenerateResponse(**result)

    def _apply_severity_clamps(self, request: GenerateRequest) -> GenerateRequest:
        """Apply automatic clamps based on severity"""
        severity = request.incident.severity

        if severity == Severity.HIGH:
            # High severity: strict guardrails
            request.sliders.memes = 0
            request.strategy.scapegoat.intensity = min(
                request.strategy.scapegoat.intensity, 40
            )
            request.strategy.risk_transfer = 0
            request.strategy.responsibility_split.brand = max(
                request.strategy.responsibility_split.brand, 0.5
            )
            request.strategy.responsibility_split.external = min(
                request.strategy.responsibility_split.external, 0.5
            )
        elif severity == Severity.MEDIUM:
            # Medium severity: moderate guardrails
            request.sliders.memes = min(request.sliders.memes, 15)
            request.strategy.responsibility_split.brand = max(
                request.strategy.responsibility_split.brand, 0.3
            )
            request.strategy.responsibility_split.external = min(
                request.strategy.responsibility_split.external, 0.7
            )

        return request

    def _validate_strategies(self, request: GenerateRequest) -> list[str]:
        """Validate and adjust strategies, return list of adjustments"""
        adjustments: list[str] = []

        # Scapegoat intensity requires evidence
        if request.strategy.scapegoat.intensity > 70:
            if not request.incident.evidence:
                request.strategy.scapegoat.intensity = 40
                adjustments.append(
                    "Reduced scapegoat intensity to 40 (from >70) due to lack of evidence"
                )

        # Profit alchemist requires concrete evidence
        if request.sliders.profit_alchemist >= 50:
            if not request.incident.evidence:
                request.sliders.profit_alchemist = 30
                adjustments.append(
                    "Reduced profit_alchemist to 30 (from >=50) due to lack of concrete evidence"
                )

        # Risk transfer requires legal hedging
        if request.sliders.risk_transfer > 0:
            if request.sliders.legal_hedging < 40:
                request.sliders.risk_transfer = 0
                adjustments.append(
                    "Disabled risk_transfer due to insufficient legal_hedging (<40)"
                )

        # High severity disables risk transfer
        if request.incident.severity == Severity.HIGH and request.sliders.risk_transfer > 0:
            request.sliders.risk_transfer = 0
            adjustments.append("Disabled risk_transfer for HIGH severity incident")

        return adjustments

    def _build_interpret_system_prompt(self) -> str:
        """Build system prompt for interpret mode"""
        return """You are the interpretation engine for Apology-as-a-Service (AaaS).

Your job is to parse messy incident inputs into structured incident records.

RULES:
1. Never fabricate facts or evidence
2. When evidence is missing, use "no evidence at this time" or "unknown"
3. Extract entities, times, and numbers into the extractions field
4. Assess severity based on harm scope and stakeholder impact
5. Identify relevant regulatory jurisdictions
6. Output valid JSON exactly matching the InterpretResponse schema

Output only JSON, no prose outside JSON."""

    def _build_interpret_user_prompt(self, request: InterpretRequest) -> str:
        """Build user prompt for interpret mode"""
        return f"""Parse this incident input into a structured record:

Text: {request.incident_input.text}
Links: {', '.join(request.incident_input.links) if request.incident_input.links else 'None'}
Files: {', '.join(request.incident_input.files) if request.incident_input.files else 'None'}

Output JSON with fields: incident, notes, extractions."""

    def _build_generate_system_prompt(self) -> str:
        """Build system prompt for generate mode"""
        return """You are the generation engine for Apology-as-a-Service (AaaS).

Your job is to generate two apology variants per channel: useful and pointless.

GLOBAL PRINCIPLES:
- Truth & Evidence First: Never assert certainty without evidence
- Duality: Always produce both useful and pointless variants
- Non-Apology Detector: When contrition ≥ 60, ban "we regret any inconvenience" without ownership
- Scapegoating Limits: Never target individuals or protected classes
- Legal Hedging ≠ Lying: Use qualifiers without contradicting facts

DETERMINISTIC MAPPINGS:
Contrition (0-100):
  0-20: neutral/indirect
  21-59: partial ownership
  ≥60: explicit "we caused/we failed" + restitution

Legal Hedging (0-100):
  0-20: plain language
  21-59: add qualifiers ("to our knowledge", "pending investigation")
  60-100: safe-harbor/force-majeure language

Memes (0-100):
  0-10: none
  11-40: subtle idiom
  41-70: tasteful unhinged
  71-100: overt memes

CHANNEL RULES:
- twitter: ≤280 chars, crisp, ownership line if contrition ≥60
- linkedin: 2-5 sentences, professional, soft CTA
- press_release: headline, lede, summary, bullets, quote, contact
- ceo_letter: 3-7 paragraphs, human, explicit responsibility if contrition ≥60
- customer_email: greeting, what happened, restitution, support, sign-off, ~120-200 words
- status_page: timeline, scope, root cause, remediation, next update

Output valid JSON exactly matching GenerateResponse schema.
Include metrics, detectors, adjustments, and rationales."""

    def _build_generate_user_prompt(self, request: GenerateRequest) -> str:
        """Build user prompt for generate mode"""
        return f"""Generate apologies for this incident:

INCIDENT:
{json.dumps(request.incident.model_dump(), indent=2)}

SLIDERS:
{json.dumps(request.sliders.model_dump(), indent=2)}

STRATEGY:
{json.dumps(request.strategy.model_dump(), indent=2)}

TONE: {request.tone.value}
CHANNELS: {', '.join(c.value for c in request.channels)}
LOCALE: {request.locale}

{f"BRAND PROFILE: {json.dumps(request.brand_profile.model_dump(), indent=2)}" if request.brand_profile else ""}

Generate drafts for ALL requested channels.
Each channel must have both useful and pointless variants.
Include metrics, detectors, adjustments, and rationales."""


# Singleton instance
llm_engine = LLMEngine()
