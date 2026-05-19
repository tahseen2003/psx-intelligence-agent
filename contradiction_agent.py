# =====================================================
#  ⚖️ CONTRADICTION AGENT — Cross-Source Conflict Detector
#  Compares multiple sources to find contradictions
#  Ranks credibility and gives resolution
# =====================================================

from config import get_completion


def detect_contradictions(sources_data):
    """
    Compare multiple sources and identify contradictions.

    Args:
        sources_data: list of dicts from ReaderAgent
                      [{"name": "file.txt", "content": "..."}, ...]

    Returns:
        str: Structured contradiction report
    """

    # Format each source with a label
    labeled_sources = ""
    for i, source in enumerate(sources_data, 1):
        labeled_sources += f"\n\n{'='*40}\n"
        labeled_sources += f"SOURCE {i}: {source['name']}\n"
        labeled_sources += f"{'='*40}\n"
        labeled_sources += source["content"]

    # Contradiction detection prompt
    prompt = f"""
You are a financial data verification specialist at PSX (Pakistan Stock Exchange).
You have received data from multiple sources. Your job is to find contradictions.

RESPOND IN THIS EXACT FORMAT:

🔍 CONTRADICTION ANALYSIS REPORT
{'='*40}

⚔️ CONTRADICTION #1:
• Source A says: [exact claim from source]
• Source B says: [conflicting claim from source]
• Impact: [How this contradiction affects investment decisions]

⚔️ CONTRADICTION #2:
• Source A says: [exact claim]
• Source B says: [conflicting claim]
• Impact: [How this affects decisions]

⚔️ CONTRADICTION #3:
(Continue if more contradictions found...)

📊 CREDIBILITY RANKING:
1. [Most credible source name] — [reason]
2. [Next source] — [reason]
3. [Least credible] — [reason]

⏰ DATA STALENESS CHECK:
• [Source name]: [Fresh / Potentially Stale] — [reason]
• [Source name]: [Fresh / Potentially Stale] — [reason]

✅ RESOLUTION:
[Clear recommendation on what data to trust and why]

🎯 CONFIDENCE LEVEL: [XX]%
[1 sentence explaining confidence in the resolution]

SOURCES TO ANALYZE:
{labeled_sources}

Find ALL contradictions. Be specific about which sources conflict.
Quote exact numbers and claims that differ between sources.
"""

    # Call Groq API
    try:
        return get_completion(prompt)
    except Exception as e:
        return f"[ERROR] Contradiction detection failed: {e}"


# ── TEST ──────────────────────────────────────────
if __name__ == "__main__":
    from reader_agent import read_all_sources

    sources = [
        "data/psx_market_report.txt",
        "data/psx_news_article.txt",
        "data/psx_stock_data.csv"
    ]

    print("\n⚖️ CONTRADICTION AGENT — Testing")
    print("=" * 50)

    # Step 1: Read sources
    data = read_all_sources(sources)

    # Step 2: Detect contradictions
    print("\n⚖️ Analyzing contradictions with Gemini...")
    report = detect_contradictions(data)

    print("\n" + "=" * 50)
    print("⚔️ CONTRADICTION REPORT:")
    print("=" * 50)
    print(report)
