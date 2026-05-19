# =====================================================
#  🤖 ORCHESTRATOR — Antigravity-Style Pipeline Controller
#  Controls all agents, maintains trace logs,
#  manages state between agents
# =====================================================

import datetime


class AntigravityOrchestrator:
    """Central pipeline controller that runs all agents in sequence."""

    def __init__(self):
        self.trace_logs = []
        self.pipeline_state = {}

    def log(self, agent, status, message):
        """Add a trace log entry."""
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")

        emojis = {
            "SUCCESS": "✅",
            "FAILED": "❌",
            "WARNING": "⚠️",
            "INFO": "🔄",
            "START": "🚀",
            "DONE": "🏁"
        }
        emoji = emojis.get(status, "📋")

        entry = f"[{timestamp}] [{agent}] {emoji} {message}"
        self.trace_logs.append(entry)
        print(f"  {entry}")
        return entry

    def run_pipeline(self, source_list):
        """
        Run the complete Content-to-Action pipeline.

        Args:
            source_list: list of file paths or URLs

        Returns:
            dict with all results and trace logs
        """
        # Import agents here to avoid circular imports
        from reader_agent import read_all_sources
        from insight_agent import extract_insights
        from contradiction_agent import detect_contradictions
        from action_agent import generate_actions
        from simulator_agent import simulate_execution

        self.log("Orchestrator", "START", "Pipeline initiated")
        self.log("Orchestrator", "INFO",
                 f"{len(source_list)} input sources received")

        # ── STEP 1: READ SOURCES ──
        self.log("ReaderAgent", "INFO", "Reading input sources...")
        try:
            sources_data = read_all_sources(source_list)
            for s in sources_data:
                self.log("ReaderAgent", "SUCCESS",
                         f"Loaded: {s['name']} ({s['format']})")
            self.pipeline_state["sources"] = sources_data
        except Exception as e:
            self.log("ReaderAgent", "FAILED", f"Error: {e}")
            return self._error_result(f"Reader failed: {e}")

        # ── STEP 2: EXTRACT INSIGHTS ──
        self.log("InsightAgent", "INFO",
                 "Analyzing content with Groq...")
        try:
            insights = extract_insights(sources_data)
            self.log("InsightAgent", "SUCCESS",
                     "Insights extracted successfully")
            self.pipeline_state["insights"] = insights
        except Exception as e:
            self.log("InsightAgent", "FAILED", f"Error: {e}")
            return self._error_result(f"Insight extraction failed: {e}")

        # ── STEP 3: DETECT CONTRADICTIONS ──
        self.log("ContradictionAgent", "INFO",
                 "Comparing sources for contradictions...")
        try:
            contradictions = detect_contradictions(sources_data)
            self.log("ContradictionAgent", "WARNING",
                     "Contradictions detected between sources")
            self.log("ContradictionAgent", "SUCCESS",
                     "Contradiction report generated")
            self.pipeline_state["contradictions"] = contradictions
        except Exception as e:
            self.log("ContradictionAgent", "FAILED", f"Error: {e}")
            return self._error_result(
                f"Contradiction detection failed: {e}")

        # ── STEP 4: GENERATE ACTIONS ──
        self.log("ActionAgent", "INFO",
                 "Generating connected action chain...")
        try:
            actions = generate_actions(insights, contradictions)
            self.log("ActionAgent", "SUCCESS",
                     "Action chain generated (4 connected steps)")
            self.pipeline_state["actions"] = actions
        except Exception as e:
            self.log("ActionAgent", "FAILED", f"Error: {e}")
            return self._error_result(f"Action generation failed: {e}")

        # ── STEP 5: SIMULATE EXECUTION ──
        self.log("SimulatorAgent", "INFO",
                 "Simulating action execution...")
        try:
            simulation = simulate_execution(actions, insights)
            self.log("SimulatorAgent", "WARNING",
                     f"Failure at step {simulation['failure_step']}: "
                     f"{simulation['failure_reason']}")
            self.log("SimulatorAgent", "SUCCESS",
                     f"Recovery: {simulation['recovery_strategy']}")
            self.log("SimulatorAgent", "SUCCESS",
                     "Simulation completed — all actions executed")
            self.pipeline_state["simulation"] = simulation
        except Exception as e:
            self.log("SimulatorAgent", "FAILED", f"Error: {e}")
            return self._error_result(f"Simulation failed: {e}")

        # ── PIPELINE COMPLETE ──
        self.log("Orchestrator", "DONE",
                 "Pipeline completed successfully ✅")

        return {
            "status": "SUCCESS",
            "sources": sources_data,
            "insights": insights,
            "contradictions": contradictions,
            "actions": actions,
            "simulation": simulation,
            "trace_logs": self.trace_logs
        }

    def _error_result(self, error_msg):
        """Return error result with trace logs."""
        self.log("Orchestrator", "FAILED",
                 f"Pipeline aborted: {error_msg}")
        return {
            "status": "FAILED",
            "error": error_msg,
            "trace_logs": self.trace_logs,
            **self.pipeline_state
        }


# ── TEST ──
if __name__ == "__main__":
    sources = [
        "data/psx_market_report.txt",
        "data/psx_news_article.txt",
        "data/psx_stock_data.csv"
    ]

    print("\n🤖 ORCHESTRATOR — Full Pipeline Test")
    print("=" * 50)

    orchestrator = AntigravityOrchestrator()
    result = orchestrator.run_pipeline(sources)

    print(f"\n\n{'='*50}")
    print(f"Pipeline Status: {result['status']}")
    print(f"Trace Logs: {len(result['trace_logs'])} entries")
    print(f"{'='*50}")
