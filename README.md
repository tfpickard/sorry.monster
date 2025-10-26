# sorry.monster - Apology-as-a-Service (AaaS)

LLM-powered apology generation platform with full control over tone, style, and sincerity.

## 🎯 Overview

**sorry.monster** is an API-first apology generation service that uses GPT-4 to create both professional and satirical apologies across multiple communication channels. It features sophisticated guardrails, risk scoring, and ethical constraints to ensure responsible output.

### Services

- **sorry.monster** - Full-featured service with UI, API, accounts, brand profiles
- **oops.ninja** - Instant "I'm Feeling Lucky" mode with minimal controls

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                         NGINX                               │
│  (TLS termination, FQDN-aware routing)                     │
└─────────────────┬───────────────────────────┬───────────────┘
                  │                           │
    ┌─────────────▼─────────────┐  ┌──────────▼──────────┐
    │  sorry.monster:443        │  │  oops.ninja:443     │
    │  ┌────────────────────┐   │  │  ┌───────────────┐  │
    │  │ Next.js Frontend   │   │  │  │ Minimal Form  │  │
    │  │ (Port 8082)       │   │  │  │ (Port 8085)   │  │
    │  └────────┬───────────┘   │  │  └───────┬───────┘  │
    │           │               │  │          │          │
    │  ┌────────▼───────────┐   │  │          │          │
    │  │ FastAPI Backend    │   │  │          │          │
    │  │ (Port 8083)       │◄──┼──┼──────────┘          │
    │  └────────┬───────────┘   │  │                     │
    └───────────┼───────────────┘  └─────────────────────┘
                │
    ┌───────────▼────────────┐
    │  LLM Engine (GPT-4)    │
    │  + Guardrails          │
    │  + Risk Scoring        │
    └────────────────────────┘

    ┌───────────────────────────────────┐
    │  PostgreSQL + pgvector   Redis    │
    │  (Brand profiles)        (Cache)  │
    └───────────────────────────────────┘
```

## 🚀 Features

### Core Capabilities
- **Dual Output**: Every generation produces both "useful" (professional) and "pointless" (satirical) variants
- **Multi-Channel**: Twitter, LinkedIn, press releases, CEO letters, customer emails, status pages
- **Guardrails**: Automatic severity-based constraints, evidence validation, scapegoat limits
- **Risk Scoring**: PR risk, legal risk, ethics score, clarity score, sincerity score
- **Brand Profiles**: Voice traits, taboo topics, legal boilerplate, exemplar paragraphs

### Control Sliders (0-100)
- **Contrition**: How much ownership/responsibility
- **Legal Hedging**: Qualifiers and safe-harbor language
- **Memes**: None → subtle → tasteful → overt
- **Accountability Evasion**: Passive voice, broadened scope
- **Profit Alchemist**: Spin failure as "learning opportunity"
- **Risk Transfer**: "Beyond our control" framing
- **Data Fog**: Contextless metrics and benchmarks
- **Pseudo-Transparency**: High-level timeline with sanitized RCA

### Advanced Strategies
- **Scapegoating**: vendor_outage, legacy_system, industry_wide, etc. (with evidence requirements)
- **Distraction Tactics**: CSR donations, carbon offsets, product teasers
- **Responsibility Split**: Brand vs. external attribution
- **Self-Credentialing**: SOC 2, ISO 27001, etc.

## 📦 Tech Stack

- **Frontend**: Next.js 14 (React 18, TypeScript, Tailwind CSS)
- **API**: FastAPI (Python 3.12)
- **LLM**: OpenAI GPT-4 Turbo
- **Database**: PostgreSQL 16 + pgvector
- **Cache**: Redis 7
- **Auth**: NextAuth.js (Google OAuth)
- **Infra**: Docker Compose, NGINX, Let's Encrypt
- **CI/CD**: GitHub Actions
- **Observability**: Sentry, OpenTelemetry

## 🛠️ Development Setup

### Prerequisites
- Node.js 22+
- Python 3.12+
- Docker & Docker Compose
- OpenAI API key

### Local Development

1. **Clone and install dependencies**:
   ```bash
   git clone https://github.com/yourusername/sorry.monster.git
   cd sorry.monster
   npm install
   ```

2. **Set up environment variables**:
   ```bash
   cp .env.example .env
   # Edit .env and add your OpenAI API key
   ```

3. **Start services**:
   ```bash
   # Start PostgreSQL and Redis
   docker compose up -d postgres redis

   # Start API backend
   cd apps/api
   pip install -r requirements.txt
   uvicorn app.main:app --reload --port 8083

   # Start frontend (new terminal)
   cd apps/frontend
   npm install
   npm run dev

   # Start oops.ninja (new terminal)
   cd apps/oops
   pip install -r requirements.txt
   uvicorn oops.app:app --reload --port 8085
   ```

4. **Access services**:
   - API: http://localhost:8083
   - Frontend: http://localhost:8082
   - Oops: http://localhost:8085

### Running Tests

```bash
# Backend tests
cd apps/api
pytest -v

# Frontend tests
cd apps/frontend
npm test

# Linting
npm run lint
ruff check apps/api
```

## 🚢 Deployment

### Port Configuration (CRITICAL)
**NEVER use ports 3000, 4000, or 8000** - these are forbidden on the shared server.

Assigned ports:
- `8082` - sorry.monster frontend (Next.js)
- `8083` - API backend (FastAPI)
- `8085` - oops.ninja instant service

### GitHub Actions CI/CD

The project uses automated deployment via GitHub Actions:

1. **PR Validation** (`.github/workflows/ci.yml`):
   - Build frontend & backend
   - Run tests
   - Lint checks
   - Security scanning (CodeQL)

2. **Auto-Deploy** (`.github/workflows/deploy.yml`):
   - Triggers on push to `main`
   - Builds artifacts
   - Deploys via rsync
   - Restarts Docker services
   - Updates NGINX configs

### Required GitHub Secrets

Configure these in **Settings → Secrets and variables → Actions**:

```
SSH_HOST          # Server hostname
SSH_USER          # Deploy user (e.g., deploy)
SSH_KEY           # Private SSH key
TARGET_DIR        # Deploy path (e.g., /home/deploy/sorry.monster)
ENV_FILE_B64      # Base64-encoded .env file
NODE_VERSION      # Optional: 22
PY_VERSION        # Optional: 3.12
```

### Server Setup

1. **Install dependencies**:
   ```bash
   sudo apt update
   sudo apt install docker.io docker-compose nginx certbot python3-certbot-nginx
   ```

2. **Obtain SSL certificates**:
   ```bash
   sudo certbot certonly --nginx -d sorry.monster -d www.sorry.monster
   sudo certbot certonly --nginx -d oops.ninja -d www.oops.ninja
   ```

3. **Deploy via GitHub Actions** or manually:
   ```bash
   cd /home/deploy/sorry.monster
   docker compose up -d
   sudo systemctl reload nginx
   ```

## 📖 API Documentation

### Interpret Endpoint

**POST** `/v1/interpret`

Parse messy incident input into structured record.

```json
{
  "mode": "interpret",
  "incident_input": {
    "text": "Our database went down for 2 hours affecting 1000 customers",
    "links": [],
    "files": []
  }
}
```

### Generate Endpoint

**POST** `/v1/generate`

Generate apology drafts with guardrails.

```json
{
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
    "evidence": ["rollback completed"]
  },
  "sliders": {
    "contrition": 65,
    "legal_hedging": 30,
    "memes": 0
  },
  "channels": ["twitter", "customer_email"],
  "tone": "earnest"
}
```

**Response**:
```json
{
  "drafts": {
    "twitter": {
      "useful": "We apologize for today's 2-hour database outage...",
      "pointless": "Oops! Our hamster fell off the wheel...",
      "attachments": [],
      "redlines": ["issues beyond our control"]
    }
  },
  "metrics": {
    "pr_risk": 0.35,
    "legal_risk": 0.15,
    "ethics_score": 0.25,
    "clarity_score": 0.80,
    "sincerity_score": 0.75
  },
  "detectors": {
    "non_apology": false,
    "scapegoat_flag": "none",
    "unverifiable_claims": []
  },
  "adjustments": ["Reduced memes to 0 for HIGH severity"],
  "rationales": ["High contrition requires explicit ownership"]
}
```

## 🔒 Security & Ethics

### Guardrails
- **High severity**: memes=0, explicit ownership required, no risk transfer
- **Medium severity**: memes capped at 15
- **Non-apology detection**: Ban "we regret any inconvenience" when contrition ≥ 60
- **Scapegoat limits**: Never target individuals or protected classes
- **Evidence requirements**: High-intensity scapegoating requires proof

### Content Moderation
- Refuse hate/violence/illegal requests
- No tragedy exploitation
- No medical/financial advice beyond boilerplate
- Automatic redaction of sensitive data

### Rate Limiting
- Anonymous: 10 requests/hour
- Authenticated: 100 requests/hour

## 📊 Monitoring

- **Health checks**: `/health` endpoints on all services
- **Metrics**: Request duration, error rates, LLM token usage
- **Logs**: Structured JSON logging
- **Alerts**: Sentry for errors, OTEL for traces

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## 📄 License

Proprietary - All rights reserved

## 🙏 Acknowledgments

- Powered by OpenAI GPT-4
- Built with FastAPI, Next.js, and modern web standards
- Inspired by the absurdity of corporate apologies

---

**Live Services**:
- 🌐 [sorry.monster](https://sorry.monster) - Full platform
- ⚡ [oops.ninja](https://oops.ninja) - Instant mode

**Support**: [GitHub Issues](https://github.com/yourusername/sorry.monster/issues)
