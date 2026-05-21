# 📈 PSX Content-to-Action Agent

**AISeekho 2026 Hackathon — Challenge 1**
**Domain: Pakistan Stock Exchange (PSX)**

## Team

| Role | Name |
|------|------|
| 🎯 **Project Leader** | **Saddam Hussain** |
| 💻 **Developer** | **Tahseen Ullah** |

## What It Does

This AI agent system reads multiple PSX market data sources, extracts financial insights, detects contradictions between sources, generates a connected chain of trading actions, and simulates their execution with failure recovery.

## Tech Stack

- **Python 3** — Core language
- **Groq API** (llama-3.1-8b-instant) — AI/LLM engine
- **Streamlit** — Frontend dashboard (Glassmorphism UI)
- **Antigravity Orchestrator** — Pipeline controller

## Agent Architecture

| Agent | Role |
|-------|------|
| 📄 ReaderAgent | Reads TXT, CSV, JSON, URL sources |
| 🔍 InsightAgent | Extracts market trends and risk analysis |
| ⚖️ ContradictionAgent | Detects conflicting claims between sources |
| ⚡ ActionAgent | Generates 3-5 connected trading actions |
| 🎬 SimulatorAgent | Simulates execution with failure + recovery |

## Setup

```bash
pip install -r requirements.txt
```

## Run

**Streamlit UI:**
```bash
streamlit run ui.py
```

**CLI Mode:**
```bash
python main.py
```

## Project Structure

```
├── config.py              # Groq API setup
├── reader_agent.py        # Multi-source reader
├── insight_agent.py       # Financial insight extraction
├── contradiction_agent.py # Cross-source contradiction detection
├── action_agent.py        # Connected action chain generator
├── simulator_agent.py     # Execution simulator + failure recovery
├── orchestrator.py        # Antigravity pipeline controller
├── main.py                # CLI runner
├── ui.py                  # Streamlit dashboard
├── requirements.txt       # Dependencies
└── data/
    ├── psx_market_report.txt
    ├── psx_stock_data.csv
    └── psx_news_article.txt
```

## Credits

- **Project Leader:** Saddam Hussain
- **Developer:** Tahseen Ullah
- **Hackathon:** AISeekho 2026 — Challenge 1
- **Powered by:** Groq API + Streamlit + Python
