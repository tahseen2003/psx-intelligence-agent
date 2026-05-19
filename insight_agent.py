# =====================================================
#  🔍 INSIGHT AGENT — Financial Insight Extractor
#  Uses Gemini to analyze PSX market data
#  Extracts trends, metrics, risks, and insights
# =====================================================

from config import get_completion


def extract_insights(sources_data):
    """
    Analyze combined source data and extract financial insights.

    Args:
        sources_data: list of dicts from ReaderAgent
                      [{"name": "file.txt", "content": "..."}, ...]

    Returns:
        str: Structured insight text
    """

    # Combine all sources into one text block
    combined_text = ""
    for source in sources_data:
        combined_text += f"\n\n--- SOURCE: {source['name']} ---\n"
        combined_text += source["content"]

    # PSX-specific insight extraction prompt
    prompt = f"""
You are a senior financial analyst at the Pakistan Stock Exchange (PSX).
Analyze the following market data from multiple sources and extract insights.

RESPOND IN THIS EXACT FORMAT:

📊 MARKET TREND:
[State: BULLISH / BEARISH / NEUTRAL]
[1-2 sentence explanation with specific numbers]

📈 KEY METRICS:
• KSE-100 Index: [value and change]
• Trading Volume: [value]
• Foreign Investment: [net buy/sell amount]
• Market Cap: [total value]

🏢 SECTOR ANALYSIS:
• Top Performing Sector: [name] — [reason with numbers]
• Weakest Sector: [name] — [reason with numbers]
• Sector to Watch: [name] — [why]

⚠️ RISK LEVEL: [LOW / MEDIUM / HIGH / CRITICAL]
[1 sentence justification]

💡 CRITICAL INSIGHT:
[One clear, actionable insight that a portfolio manager must act on TODAY]

🎯 RECOMMENDATION:
[1-2 sentences on what action to take based on the analysis]

DATA ANALYZED:
{combined_text}
"""

    # Call Groq API
    try:
        return get_completion(prompt)
    except Exception as e:
        return f"[ERROR] Insight extraction failed: {e}"


# ── TEST ──────────────────────────────────────────
if __name__ == "__main__":
    from reader_agent import read_all_sources

    sources = [
        "data/psx_market_report.txt",
        "data/psx_stock_data.csv"
    ]

    print("\n🔍 INSIGHT AGENT — Testing")
    print("=" * 50)

    # Step 1: Read sources
    data = read_all_sources(sources)

    # Step 2: Extract insights
    print("\n🔍 Extracting insights with Gemini...")
    insights = extract_insights(data)

    print("\n" + "=" * 50)
    print("📊 EXTRACTED INSIGHTS:")
    print("=" * 50)
    print(insights)
