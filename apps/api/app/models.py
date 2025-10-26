"""Pydantic models for API request/response schemas"""

from enum import Enum
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Severity(str, Enum):
    """Incident severity levels"""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class RiskLevel(str, Enum):
    """Risk assessment levels"""

    INFORMATIONAL = "informational"
    OPERATIONAL = "operational"
    REGULATORY = "regulatory"
    REPUTATIONAL = "reputational"
    FINANCIAL = "financial"


class Channel(str, Enum):
    """Communication channels"""

    TWITTER = "twitter"
    LINKEDIN = "linkedin"
    PRESS_RELEASE = "press_release"
    CEO_LETTER = "ceo_letter"
    CUSTOMER_EMAIL = "customer_email"
    STATUS_PAGE = "status_page"


class Tone(str, Enum):
    """Apology tones"""

    EARNEST = "earnest"
    WARM = "warm"
    DRY = "dry"
    STOIC = "stoic"
    CHEEKY = "cheeky"


class ScapegoatType(str, Enum):
    """Allowed scapegoat types"""

    VENDOR_OUTAGE = "vendor_outage"
    LEGACY_SYSTEM = "legacy_system"
    INDUSTRY_WIDE = "industry_wide"
    UNEXPECTED_DEPENDENCY = "unexpected_dependency"
    WEATHER = "weather"
    UNKNOWN_ROOT_CAUSE = "unknown_root_cause"


class DistractionType(str, Enum):
    """Distraction tactics"""

    CSR_DONATION = "csr_donation"
    CARBON_OFFSET_MENTION = "carbon_offset_mention"
    PRODUCT_ANNOUNCEMENT_TEASE = "product_announcement_tease"
    COMMUNITY_HIGHLIGHT = "community_highlight"


class IncidentInput(BaseModel):
    """Raw incident input for interpretation"""

    text: str = Field(..., description="Raw description, quotes, pasted tweets, links")
    links: list[str] = Field(default_factory=list, description="URL links")
    files: list[str] = Field(default_factory=list, description="File metadata references")


class Incident(BaseModel):
    """Structured incident record"""

    summary: str = Field(..., description="Brief incident summary")
    who: list[str] = Field(default_factory=list, description="Affected parties")
    what: str = Field(..., description="What happened")
    when: str = Field(default="unknown", description="When it happened (ISO8601 or 'unknown')")
    harm: str = Field(..., description="Description of harm caused")
    stakeholders: list[str] = Field(
        default_factory=lambda: ["customers"], description="Affected stakeholder groups"
    )
    severity: Severity = Field(default=Severity.LOW, description="Incident severity")
    jurisdictions: list[str] = Field(
        default_factory=list, description="Relevant regulatory jurisdictions"
    )
    risk_level: Optional[RiskLevel] = Field(None, description="Risk assessment")
    evidence: list[str] = Field(default_factory=list, description="Evidence of remediation")


class Sliders(BaseModel):
    """Tone and style control sliders (0-100)"""

    contrition: int = Field(default=50, ge=0, le=100)
    legal_hedging: int = Field(default=30, ge=0, le=100)
    memes: int = Field(default=0, ge=0, le=100)
    accountability_evasion: int = Field(default=0, ge=0, le=100)
    profit_alchemist: int = Field(default=0, ge=0, le=100)
    risk_transfer: int = Field(default=0, ge=0, le=100)
    data_fog: int = Field(default=0, ge=0, le=100)
    pseudo_transparency: int = Field(default=0, ge=0, le=100)


class ScapegoatStrategy(BaseModel):
    """Scapegoat configuration"""

    type: Optional[ScapegoatType] = None
    intensity: int = Field(default=0, ge=0, le=100)


class DistractionStrategy(BaseModel):
    """Distraction tactics configuration"""

    type: Optional[DistractionType] = None
    intensity: int = Field(default=0, ge=0, le=100)


class ResponsibilitySplit(BaseModel):
    """Brand vs external responsibility split"""

    brand: float = Field(default=0.5, ge=0.0, le=1.0)
    external: float = Field(default=0.5, ge=0.0, le=1.0)

    @field_validator("external")
    @classmethod
    def validate_split(cls, v: float, info: Any) -> float:
        """Ensure brand + external = 1.0"""
        brand = info.data.get("brand", 0.5)
        if abs((brand + v) - 1.0) > 0.01:
            raise ValueError("brand + external must equal 1.0")
        return v


class Strategy(BaseModel):
    """Advanced apology strategies"""

    scapegoat: ScapegoatStrategy = Field(default_factory=ScapegoatStrategy)
    distraction: DistractionStrategy = Field(default_factory=DistractionStrategy)
    responsibility_split: ResponsibilitySplit = Field(default_factory=ResponsibilitySplit)
    victimless_frame: bool = Field(default=False)
    self_credentialing: list[str] = Field(default_factory=list)


class VoiceTraits(BaseModel):
    """Brand voice characteristics"""

    reading_level: Literal["middle", "high_school", "college"] = "high_school"
    cadence: Literal["short", "balanced", "long"] = "balanced"
    keywords: list[str] = Field(default_factory=list)


class BrandProfile(BaseModel):
    """Brand-specific configuration"""

    name: str
    values: list[str] = Field(default_factory=list)
    taboo_topics: list[str] = Field(default_factory=list)
    legal_boilerplate: str = ""
    voice_traits: VoiceTraits = Field(default_factory=VoiceTraits)
    exemplar_paragraphs: list[str] = Field(default_factory=list)


class InterpretRequest(BaseModel):
    """Request for incident interpretation"""

    mode: Literal["interpret"] = "interpret"
    incident_input: IncidentInput


class GenerateRequest(BaseModel):
    """Request for apology generation"""

    mode: Literal["generate"] = "generate"
    incident: Incident
    sliders: Sliders = Field(default_factory=Sliders)
    strategy: Strategy = Field(default_factory=Strategy)
    tone: Tone = Field(default=Tone.EARNEST)
    channels: list[Channel] = Field(default_factory=lambda: [Channel.TWITTER])
    brand_profile: Optional[BrandProfile] = None
    locale: str = Field(default="en-US")


class InterpretResponse(BaseModel):
    """Interpretation result"""

    incident: Incident
    notes: list[str] = Field(default_factory=list)
    extractions: dict[str, list[str]] = Field(default_factory=dict)


class ChannelDraft(BaseModel):
    """Apology draft for a specific channel"""

    useful: str
    pointless: str
    attachments: list[str] = Field(default_factory=list)
    redlines: list[str] = Field(default_factory=list)


class Metrics(BaseModel):
    """Risk and quality metrics"""

    pr_risk: float = Field(ge=0.0, le=1.0)
    legal_risk: float = Field(ge=0.0, le=1.0)
    ethics_score: float = Field(ge=0.0, le=1.0)
    clarity_score: float = Field(ge=0.0, le=1.0)
    sincerity_score: float = Field(ge=0.0, le=1.0)


class Detectors(BaseModel):
    """Content detection flags"""

    non_apology: bool = False
    scapegoat_flag: str = "none"
    unverifiable_claims: list[str] = Field(default_factory=list)


class GenerateResponse(BaseModel):
    """Generation result"""

    drafts: dict[str, ChannelDraft]
    metrics: Metrics
    detectors: Detectors
    adjustments: list[str] = Field(default_factory=list)
    rationales: list[str] = Field(default_factory=list)


class HealthResponse(BaseModel):
    """Health check response"""

    status: str
    version: str
    timestamp: str


class LuckyRequest(BaseModel):
    """I'm Feeling Lucky - minimal instant mode request"""

    summary: str = Field(..., description="Brief incident summary")
    what: str = Field(..., description="What happened")
    harm: str = Field(..., description="Harm caused")
    severity: Severity = Field(default=Severity.MEDIUM, description="Incident severity")


class LuckyChannelOutput(BaseModel):
    """Simplified channel output for lucky mode"""

    useful: str
    pointless: str


class LuckyRisk(BaseModel):
    """Simplified risk metrics"""

    pr_risk: float = Field(ge=0.0, le=1.0)
    sincerity: float = Field(ge=0.0, le=1.0)


class LuckyResponse(BaseModel):
    """I'm Feeling Lucky response - simplified output"""

    twitter: LuckyChannelOutput
    customer_email: LuckyChannelOutput
    risk: LuckyRisk
    watermark: str = "Generated by oops.ninja"
