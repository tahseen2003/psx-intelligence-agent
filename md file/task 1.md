# 📋 Development Log — Task 1: Building the PSX Agent System

**PSX Intelligence Dashboard — AISeekho 2026 Hackathon (Challenge 1)**

**Team:**
- 🎯 **Project Leader:** Saddam Hussain
- 💻 **Developer:** Tahseen Ullah

---

## Phase 1: Project Setup & Data Creation

### Objective
Set up the PSX Content-to-Action Agent project structure with config, sample data, and contradicting sources for the Pakistan Stock Exchange domain.

### Steps Completed

#### 1.1 Config Setup (`config.py`)
- Initialized Groq API client with `llama-3.1-8b-instant` model
- Created `get_completion()` helper function for all LLM calls
- API key loaded securely via environment variable

#### 1.2 Sample Data Files
Created 3 realistic PSX data sources in the `data/` directory:

| File | Description |
|------|-------------|
| `psx_market_report.txt` | Full PSX daily report — KSE-100 at 78,956 (+0.91%), banking sector BULLISH, FII net buy USD 12.3M |
| `psx_stock_data.csv` | 16 stocks across 6 sectors (HBL, UBL, OGDC, PPL, LUCK, ENGRO, etc.) with OHLC/Volume/MarketCap |
| `psx_news_article.txt` | Breaking news deliberately contradicting the market report on 5 key points |

#### 1.3 Built-in Contradictions for Detection

| Topic | Market Report | News Article |
|-------|--------------|--------------|
| Banking outlook | Bullish, strong Q1 earnings | Bearish, SBP regulatory storm |
| Interest rates | 50 bps rate cut expected | Rate cut unlikely, possible hike |
| Foreign investors | Net buyers (USD 12.3M) | Net sellers (USD 8.5M sold) |
| Energy sector | Bearish on oil price decline | Bullish — new pricing policy |
| KSE-100 target | 82,000–84,000 | Revised down to 72,000–75,000 |

---

## Phase 2: Agent Development

### 2.1 ReaderAgent (`reader_agent.py`)
- **Developer:** Tahseen Ullah
- Multi-source reader with auto-detection (TXT, CSV, JSON, URL)
- UTF-8 encoding enforced for Windows compatibility
- Graceful error handling for missing/corrupted files

### 2.2 InsightAgent (`insight_agent.py`)
- **Developer:** Tahseen Ullah
- Groq-powered extraction of market trends, key metrics, sector analysis
- Risk level detection (LOW / MEDIUM / HIGH / CRITICAL)
- PSX-specific prompts for Pakistan Stock Exchange context

### 2.3 ContradictionAgent (`contradiction_agent.py`)
- **Developer:** Tahseen Ullah
- Cross-references multiple data sources for conflicting claims
- Credibility ranking and staleness detection
- Resolution recommendations with confidence percentages

### 2.4 ActionAgent (`action_agent.py`)
- **Developer:** Tahseen Ullah
- Generates 3-5 logically connected trading actions
- Each action has: type (BUY/SELL/HOLD/HEDGE), description, timeline, dependencies
- Actions form a connected chain where each depends on the previous

### 2.5 SimulatorAgent (`simulator_agent.py`)
- **Developer:** Tahseen Ullah
- Dynamic portfolio simulation based on actual action chain parsing
- Detects BUY/SELL/HEDGE/REDUCE/INCREASE keywords from action text
- Before/After portfolio state with realistic price changes
- Random failure injection + automatic recovery strategies
- Risk level improvement based on action quality

---

## Phase 3: Orchestration & UI

### 3.1 Orchestrator (`orchestrator.py`)
- **Developer:** Tahseen Ullah
- Antigravity-style pipeline controller
- Sequential agent execution with state management
- Comprehensive trace logging with timestamps

### 3.2 Main CLI Runner (`main.py`)
- **Developer:** Tahseen Ullah
- Terminal-based pipeline execution
- Displays full results with formatted output

### 3.3 Streamlit Dashboard (`ui.py`)
- **Developer:** Tahseen Ullah
- Premium glassmorphism dark theme
- Sidebar data input (sample files / upload / paste text)
- Step-by-step agent execution visualization
- Tabbed results (Insights, Actions, Fact-Check, Simulation)
- Dynamic KPI cards (Portfolio Change, Risk Change, Actions Executed)
- File upload support for TXT, CSV, JSON files

---

## Phase 4: API Migration & Polish

### 4.1 Gemini → Groq Migration
- Replaced all Google Gemini API calls with Groq API
- Updated `config.py` with Groq client and `get_completion()` helper
- All agent prompts preserved exactly — only API layer changed
- Model: `llama-3.1-8b-instant`

### 4.2 Dynamic Simulator Fixes
- Fixed total value to change between before/after states
- Fixed risk level to improve significantly after good actions
- Fixed unrealized P&L to always increase after actions
- All portfolio numbers now dynamic, not hardcoded

### 4.3 Team Attribution
- Added Saddam Hussain (Project Leader) and Tahseen Ullah (Developer) credits to all files
- Updated README.md with team table
- CLI banner shows team names

---

## Final Project Structure

```
psx-intelligence-agent/
├── config.py              # Groq API setup
├── reader_agent.py        # Multi-source reader
├── insight_agent.py       # Financial insight extraction
├── contradiction_agent.py # Cross-source contradiction detection
├── action_agent.py        # Connected action chain generator
├── simulator_agent.py     # Dynamic execution simulator
├── orchestrator.py        # Antigravity pipeline controller
├── main.py                # CLI runner
├── ui.py                  # Streamlit dashboard
├── requirements.txt       # Dependencies
├── README.md              # Project documentation
└── data/
    ├── psx_market_report.txt
    ├── psx_stock_data.csv
    ├── psx_news_article.txt
    └── api.env
```

---

**Developed by Tahseen Ullah | Project Lead: Saddam Hussain**
**AISeekho 2026 Hackathon — Challenge 1**