# =====================================================
#  🚀 MAIN — CLI Pipeline Runner
#  Run the full Content-to-Action pipeline from terminal
# =====================================================

from orchestrator import AntigravityOrchestrator


def main():
    print("\n" + "=" * 55)
    print("  📈 PSX CONTENT-TO-ACTION AGENT")
    print("  AISeekho 2026 Hackathon — Challenge 1")
    print("  Domain: Pakistan Stock Exchange (PSX)")
    print("=" * 55)

    # Define input sources
    sources = [
        "data/psx_market_report.txt",
        "data/psx_news_article.txt",
        "data/psx_stock_data.csv"
    ]

    print(f"\n📂 Input Sources: {len(sources)} files")
    for s in sources:
        print(f"   • {s}")

    # Run the full pipeline
    print("\n" + "─" * 55)
    print("  🤖 STARTING ANTIGRAVITY PIPELINE")
    print("─" * 55)

    orchestrator = AntigravityOrchestrator()
    result = orchestrator.run_pipeline(sources)

    # Display results
    if result["status"] == "SUCCESS":
        print("\n" + "=" * 55)
        print("  🔍 EXTRACTED INSIGHTS")
        print("=" * 55)
        print(result["insights"])

        print("\n" + "=" * 55)
        print("  ⚖️ CONTRADICTION REPORT")
        print("=" * 55)
        print(result["contradictions"])

        print("\n" + "=" * 55)
        print("  ⚡ ACTION CHAIN")
        print("=" * 55)
        print(result["actions"])

        print(result["simulation"]["before_state"])
        print(result["simulation"]["execution_log"])
        print(result["simulation"]["after_state"])

        print("\n" + "=" * 55)
        print("  🤖 AGENT TRACE LOG")
        print("=" * 55)
        for log in result["trace_logs"]:
            print(f"  {log}")

        print("\n" + "=" * 55)
        print("  ✅ PIPELINE COMPLETE")
        print("=" * 55)
    else:
        print(f"\n❌ Pipeline Failed: {result.get('error', 'Unknown')}")


if __name__ == "__main__":
    main()
