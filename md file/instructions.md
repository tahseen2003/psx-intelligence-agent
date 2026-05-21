# 🚀 Instructions: Setup and Execution

**PSX Intelligence Dashboard — AISeekho 2026 Hackathon (Challenge 1)**

**Team:**
- 🎯 **Project Leader:** Saddam Hussain
- 💻 **Developer:** Tahseen Ullah

---

Follow these step-by-step instructions to run the PSX Intelligence Dashboard locally on your machine.

## Prerequisites
- Python 3.8 or higher
- A [Groq API Key](https://console.groq.com/) for the LLM engine

## 1. Installation
1. Clone the repository to your local machine:
   ```bash
   git clone https://github.com/tahseen2003/psx-intelligence-agent.git
   cd psx-intelligence-agent
   ```
2. Install the required Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
   *(Ensure `streamlit`, `groq`, and `python-dotenv` are installed).*

## 2. Configuration
1. Navigate to the `data/` directory.
2. Ensure you have a file named `api.env` inside the `data/` folder.
3. Open `data/api.env` and add your Groq API key:
   ```env
   GROQ_API_KEY=gsk_your_api_key_here
   ```
   *(Note: The `config.py` file looks specifically for this path to load the key).*

## 3. Running the Application
To start the Streamlit server, run the following command in your terminal from the root of the project:
```bash
python -m streamlit run ui.py
```
This will start a local web server.

## 4. Testing the Application
1. Open your browser to the local URL provided in the terminal (usually `http://localhost:8501`).
2. On the left sidebar, select **"📁 Sample PSX Data"** to load the pre-configured market reports.
3. Click the **"🚀 Execute Agents"** button.
4. Watch the pipeline run! You will see the agents execute step-by-step, followed by a simulated portfolio return and detailed reports in the tabs below.

## Agent Traces and Logs
The system provides real-time visibility into the agentic workflow:
* **ReaderAgent:** Successfully ingested raw inputs (market data and news).
* **InsightAgent:** Successfully extracted financial indicators and metrics.
* **ContradictionAgent & ActionAgent:** Formulated risk profiles and decisions.
* **SimulatorAgent:** Successfully completed the simulation loop with failure recovery.

## Baseline Comparison
* **Baseline Approach:** Manual analysis of financial sheets, news trends, and data cross-referencing takes roughly 30 to 45 minutes for a human analyst.
* **Our Solution:** The automated multi-agent pipeline completes the entire processing, asset evaluation, and analytical summary in under 10 seconds.

## Robustness Evidence
The application implements explicit try-catch error handling in every agent module. If any single agent fails (e.g., API timeout, malformed input), the orchestrator catches the error, logs it in the trace, and reports a clean failure message to the UI without crashing.

---

**Developed by Tahseen Ullah | Project Lead: Saddam Hussain**
**AISeekho 2026 Hackathon — Challenge 1**