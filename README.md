<<<<<<< HEAD
# 📈 PSX Content-to-Action Agent

**AISeekho 2026 Hackathon — Challenge 1**
**Domain: Pakistan Stock Exchange (PSX)**

## What It Does

This AI agent system reads multiple PSX market data sources, extracts financial insights, detects contradictions between sources, generates a connected chain of trading actions, and simulates their execution with failure recovery.

## Tech Stack

- **Python** — Core language
- **llama-3.1-8b-instant** — AI/LLM engine
- **Streamlit** — Frontend dashboard
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
├── config.py              # Gemini API setup
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

## Team

Built for AISeekho 2026 Hackathon — Challenge 1
=======
# psx-intelligence-agent
>>>>>>> 4021a62070de7993aeb60f8b9c7276fb615dab22
