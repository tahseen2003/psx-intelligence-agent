# =====================================================
#  ⚡ ACTION AGENT — Connected Action Chain Generator
#  Generates 3-5 logically connected trading actions
#  Each action depends on the previous one
# =====================================================

from groq import Groq
import os
import streamlit as st

def get_completion(prompt):
    try:
        api_key = st.secrets["GROQ_API_KEY"]
    except:
        api_key = os.getenv("GROQ_API_KEY")
    
    client = Groq(api_key=api_key)
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}]
    )
    return response.choices[0].message.content


def generate_actions(insights, contradictions):
    """
    Generate a connected chain of 3-5 trading actions.

    Args:
        insights: str from InsightAgent
        contradictions: str from ContradictionAgent

    Returns:
        str: Structured action chain
    """

    prompt = f"""
You are a senior portfolio manager at a Pakistani brokerage firm.
Based on the market insights and contradiction analysis below,
generate a CONNECTED CHAIN of exactly 4 trading actions.

RULES:
- Each action MUST depend on the previous action
- Actions must be logically connected (not random)
- Consider the contradictions when making decisions
- Be specific with stock names (HBL, UBL, OGDC, PPL, LUCK, ENGRO)
- Use realistic percentages and amounts

RESPOND IN THIS EXACT FORMAT:

ACTION CHAIN — PSX Portfolio Adjustment

ACTION 1:
Type: [BUY / SELL / HOLD / HEDGE / REBALANCE]
Action: [1-sentence with specific stock and percentage]
Who: [Portfolio Manager / Risk Team / Compliance / Trading Desk]
Timeline: [Immediately / Today / This Week]
Depends On: None — first action
Expected Outcome: [Quantified result]

ACTION 2:
Type: [BUY / SELL / HOLD / HEDGE / REBALANCE]
Action: [connects to Action 1]
Who: [responsible party]
Timeline: [when]
Depends On: Action 1 — [why]
Expected Outcome: [Quantified result]

ACTION 3:
Type: [BUY / SELL / HOLD / HEDGE / REBALANCE]
Action: [connects to Action 1 or 2]
Who: [responsible party]
Timeline: [when]
Depends On: Action 1/2 — [why]
Expected Outcome: [Quantified result]

ACTION 4:
Type: [BUY / SELL / HOLD / HEDGE / REBALANCE]
Action: [connects to previous actions]
Who: [responsible party]
Timeline: [when]
Depends On: Action 2/3 — [why]
Expected Outcome: [Quantified result]

CHAIN SUMMARY:
[2-3 sentences on overall strategy]

MARKET INSIGHTS:
{insights}

CONTRADICTION ANALYSIS:
{contradictions}
"""

    try:
        return get_completion(prompt)
    except Exception as e:
        return f"[ERROR] Action generation failed: {e}"


# ── TEST ──
if __name__ == "__main__":
    from reader_agent import read_all_sources
    from insight_agent import extract_insights
    from contradiction_agent import detect_contradictions

    sources = [
        "data/psx_market_report.txt",
        "data/psx_news_article.txt",
        "data/psx_stock_data.csv"
    ]

    print("\n⚡ ACTION AGENT — Testing")
    print("=" * 50)

    data = read_all_sources(sources)

    print("\n🔍 Extracting insights...")
    insights = extract_insights(data)

    print("\n⚖️ Detecting contradictions...")
    contradictions = detect_contradictions(data)

    print("\n⚡ Generating action chain...")
    actions = generate_actions(insights, contradictions)

    print("\n" + "=" * 50)
    print("⚡ ACTION CHAIN:")
    print("=" * 50)
    print(actions)
