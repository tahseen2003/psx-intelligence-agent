# 🤖 Developer Walkthrough: PSX Intelligence Agent

**PSX Intelligence Dashboard — AISeekho 2026 Hackathon (Challenge 1)**

**Team:**
- 🎯 **Project Leader:** Saddam Hussain
- 💻 **Developer:** Tahseen Ullah

---

This document explains the internal architecture and flow of the PSX Intelligence Agent pipeline. The system uses a modular, multi-agent approach to process market data and simulate actions.

## Architecture Overview

The system is orchestrated by a central controller that hands off data sequentially to specialized agents. Each agent is responsible for a single, focused task, ensuring high modularity and clean separation of concerns.

### 1. `ui.py` (The Frontend)
- Built with Streamlit, this file serves as the interactive dashboard.
- It features a premium "glassmorphism" dark theme and handles all user inputs (file uploads, text pasting, sample data selection).
- It initiates the pipeline via the `AntigravityOrchestrator` when the user clicks "Execute Agents" and visualizes the step-by-step progress using `st.status`.

### 2. `orchestrator.py` (The Controller)
- Serves as the central brain of the pipeline.
- It manages the state and flow of data between the various specialized agents.
- Handles error catching and execution tracing.
- Developed by **Tahseen Ullah** under the guidance of **Saddam Hussain**.

### 3. The Agent Sequence

#### A. `reader_agent.py` (Data Ingestion)
- **Role**: Reads the raw data sources (TXT, CSV, JSON, or raw text).
- **Functionality**: Parses the files into a unified format that the LLM can easily consume.
- **Developer**: Tahseen Ullah

#### B. `insight_agent.py` (Analysis)
- **Role**: The primary analytical brain.
- **Functionality**: Receives the raw text from the reader and uses the Groq API (`config.py`) to extract structured financial insights (bullish/bearish indicators, sector performance, etc.).
- **Developer**: Tahseen Ullah

#### C. `contradiction_agent.py` (Fact-Checking)
- **Role**: Risk mitigation and cross-referencing.
- **Functionality**: Analyzes the insights and the raw data to detect conflicting signals (e.g., if the news article suggests buying, but the stock data shows a massive sell-off).
- **Developer**: Tahseen Ullah

#### D. `action_agent.py` (Decision Making)
- **Role**: Strategy synthesis.
- **Functionality**: Takes the extracted insights and detected contradictions to build a logical, multi-step action chain for managing a hypothetical PSX portfolio.
- **Developer**: Tahseen Ullah

#### E. `simulator_agent.py` (Execution Simulation)
- **Role**: Safe environment testing.
- **Functionality**: Simulates the execution of the generated action chain. It tracks the "Before" and "After" states of the portfolio, logs the execution steps, calculates the financial impact (PKR change), and determines shifts in the overall risk profile. It can also simulate failure and recovery strategies.
- **Developer**: Tahseen Ullah

## Configuration & LLM Connection
- **`config.py`**: Initializes the Groq client. It securely loads the API key from `data/api.env` using `python-dotenv`. All agents that require LLM capabilities import the `get_completion` function from this module to communicate with `llama-3.1-8b-instant`.

## Data Flow Diagram

```
Input Sources (TXT/CSV/JSON)
        │
        ▼
  ┌─────────────┐
  │ ReaderAgent  │  → Reads & normalizes data
  └──────┬──────┘
         │
         ▼
  ┌──────────────┐     ┌─────────────────────┐
  │ InsightAgent │     │ ContradictionAgent   │
  │  (Analysis)  │     │  (Fact-Checking)     │
  └──────┬───────┘     └──────────┬───────────┘
         │                        │
         └────────┬───────────────┘
                  │
                  ▼
         ┌──────────────┐
         │ ActionAgent  │  → Generates trading actions
         └──────┬───────┘
                │
                ▼
        ┌───────────────┐
        │ SimulatorAgent│  → Simulates execution
        └───────────────┘
                │
                ▼
        📊 Results Dashboard
```

---

**Developed by Tahseen Ullah | Project Lead: Saddam Hussain**
**AISeekho 2026 Hackathon — Challenge 1**
