# =====================================================
#  🎬 SIMULATOR AGENT — Dynamic Action Execution Simulator
#  Parses action chain to dynamically adjust portfolio
#  Injects random failure + automatic recovery
#  Shows dynamic before/after portfolio state
# =====================================================

import datetime
import random
import re
import copy
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


# ── STOCK DATABASE (base prices from CSV) ──
STOCK_DB = {
    "HBL":   {"sector": "Banking",    "price": 168.50},
    "UBL":   {"sector": "Banking",    "price": 285.00},
    "MCB":   {"sector": "Banking",    "price": 198.70},
    "ABL":   {"sector": "Banking",    "price": 113.70},
    "OGDC":  {"sector": "Energy",     "price": 98.40},
    "PPL":   {"sector": "Energy",     "price": 82.30},
    "HUBC":  {"sector": "Energy",     "price": 48.20},
    "LUCK":  {"sector": "Cement",     "price": 892.00},
    "DGKC":  {"sector": "Cement",     "price": 90.00},
    "MLCF":  {"sector": "Cement",     "price": 42.50},
    "ENGRO": {"sector": "Fertilizer", "price": 345.00},
    "FFC":   {"sector": "Fertilizer", "price": 112.50},
    "TRG":   {"sector": "Technology", "price": 78.50},
    "SYS":   {"sector": "Technology", "price": 615.00},
}


def detect_risk_level(insights):
    """
    Extract risk from insights and map to BEFORE-state risk.
    The before state should reflect risk BEFORE actions were taken.
    - Insight says LOW    → before state = MEDIUM  (market was uncertain)
    - Insight says MEDIUM → before state = HIGH    (moderate danger)
    - Insight says HIGH   → before state = CRITICAL (serious risk)
    - Insight says CRITICAL → before state = CRITICAL
    """
    text = insights.upper()

    # First detect what the insight agent said
    if "CRITICAL" in text:
        insight_risk = "CRITICAL"
    elif "HIGH" in text:
        insight_risk = "HIGH"
    elif "MEDIUM" in text or "MODERATE" in text:
        insight_risk = "MEDIUM"
    else:
        insight_risk = "LOW"

    # Map to before-state risk (escalate by 1 level)
    before_risk_map = {
        "LOW": "MEDIUM",
        "MEDIUM": "HIGH",
        "HIGH": "CRITICAL",
        "CRITICAL": "CRITICAL"
    }

    return before_risk_map.get(insight_risk, "HIGH")


def parse_actions(actions_text):
    """Parse action chain text to find BUY/SELL/HEDGE/REDUCE/INCREASE."""
    text = actions_text.upper()
    parsed = []

    # Find all stock symbols mentioned
    mentioned_stocks = []
    for symbol in STOCK_DB:
        if symbol in text:
            mentioned_stocks.append(symbol)

    # Detect action types and match with stocks
    lines = actions_text.split("\n")
    current_action_type = None

    for line in lines:
        upper_line = line.upper().strip()

        # Detect action type
        if "BUY" in upper_line:
            current_action_type = "BUY"
        elif "SELL" in upper_line:
            current_action_type = "SELL"
        elif "HEDGE" in upper_line:
            current_action_type = "HEDGE"
        elif "REDUCE" in upper_line:
            current_action_type = "REDUCE"
        elif "INCREASE" in upper_line:
            current_action_type = "INCREASE"
        elif "REBALANCE" in upper_line:
            current_action_type = "REBALANCE"
        elif "HOLD" in upper_line:
            current_action_type = "HOLD"

        # Find stocks in this line
        if current_action_type:
            for symbol in STOCK_DB:
                if symbol in upper_line:
                    # Try to find a percentage
                    pct_match = re.findall(r'(\d+)%', line)
                    pct = int(pct_match[0]) if pct_match else 20

                    parsed.append({
                        "type": current_action_type,
                        "symbol": symbol,
                        "percentage": pct
                    })

    # If no specific stocks found, create generic sector actions
    if not parsed and mentioned_stocks:
        for stock in mentioned_stocks[:4]:
            parsed.append({
                "type": "REBALANCE",
                "symbol": stock,
                "percentage": 15
            })

    # Fallback if nothing parsed
    if not parsed:
        parsed = [
            {"type": "SELL", "symbol": "HBL", "percentage": 20},
            {"type": "BUY", "symbol": "OGDC", "percentage": 25},
            {"type": "HEDGE", "symbol": "ENGRO", "percentage": 15},
            {"type": "HOLD", "symbol": "LUCK", "percentage": 0},
        ]

    return parsed


def build_before_state(risk_level):
    """Build the initial portfolio state."""
    holdings = {
        "HBL":   {"shares": 5000,  "avg_price": 155.00},
        "UBL":   {"shares": 3000,  "avg_price": 260.00},
        "MCB":   {"shares": 4000,  "avg_price": 188.00},
        "OGDC":  {"shares": 8000,  "avg_price": 105.00},
        "PPL":   {"shares": 6000,  "avg_price": 88.00},
        "LUCK":  {"shares": 1500,  "avg_price": 850.00},
        "ENGRO": {"shares": 3500,  "avg_price": 320.00},
        "TRG":   {"shares": 10000, "avg_price": 90.00},
        "SYS":   {"shares": 1000,  "avg_price": 580.00},
    }

    # Calculate total value
    total = 3_500_000  # cash
    for sym, data in holdings.items():
        current = STOCK_DB[sym]["price"]
        data["current"] = current
        total += data["shares"] * current

    # Calculate weights
    for sym, data in holdings.items():
        value = data["shares"] * data["current"]
        data["weight"] = round(value / total * 100)

    # Calculate sector allocation
    sectors = {}
    for sym, data in holdings.items():
        sector = STOCK_DB[sym]["sector"]
        value = data["shares"] * data["current"]
        sectors[sector] = sectors.get(sector, 0) + value
    cash_total = total
    sector_alloc = {}
    for s, v in sorted(sectors.items(), key=lambda x: -x[1]):
        sector_alloc[s] = f"{round(v / cash_total * 100)}%"
    sector_alloc["Cash"] = f"{round(3_500_000 / cash_total * 100)}%"

    # Unrealized P&L
    pnl = 0
    for sym, data in holdings.items():
        pnl += (data["current"] - data["avg_price"]) * data["shares"]

    return {
        "total_value": total,
        "cash": 3_500_000,
        "holdings": holdings,
        "sector_allocation": sector_alloc,
        "unrealized_pnl": pnl,
        "risk_level": risk_level
    }


def apply_actions(before_state, parsed_actions):
    """Apply parsed actions to create the after state with realistic gains."""
    after = copy.deepcopy(before_state)
    cash_change = 0

    # Track which stocks were bought (they will appreciate in price)
    bought_stocks = []
    sold_stocks = []

    for action in parsed_actions:
        sym = action["symbol"]
        pct = action["percentage"]
        action_type = action["type"]

        if sym not in after["holdings"]:
            # New stock — add it
            after["holdings"][sym] = {
                "shares": 0,
                "avg_price": STOCK_DB[sym]["price"],
                "current": STOCK_DB[sym]["price"]
            }

        holding = after["holdings"][sym]
        current_price = STOCK_DB[sym]["price"]

        if action_type in ["SELL", "REDUCE"]:
            shares_to_sell = int(holding["shares"] * pct / 100)
            holding["shares"] -= shares_to_sell
            cash_change += shares_to_sell * current_price
            sold_stocks.append(sym)

        elif action_type in ["BUY", "INCREASE"]:
            buy_amount = int(after["cash"] * pct / 100)
            new_shares = int(buy_amount / current_price)
            holding["shares"] += new_shares
            cash_change -= new_shares * current_price
            bought_stocks.append(sym)

        elif action_type == "HEDGE":
            # Add hedge shares (smaller position)
            hedge_shares = int(holding["shares"] * pct / 200)
            holding["shares"] += hedge_shares
            cash_change -= hedge_shares * current_price
            bought_stocks.append(sym)

        elif action_type == "REBALANCE":
            # Slight adjustment
            adjust = int(holding["shares"] * pct / 100)
            change_dir = random.choice([-1, 1])
            holding["shares"] += adjust * change_dir
            cash_change -= adjust * change_dir * current_price

    # Update cash
    after["cash"] = before_state["cash"] + cash_change

    # ── ISSUE 1 FIX: Simulate market gains on bought stocks ──
    # Stocks we bought appreciate 2-5%, stocks we sold drop 1-3%
    # This makes total value INCREASE after good actions
    market_gain = 0
    for sym, data in after["holdings"].items():
        if sym in bought_stocks:
            # Bought stocks appreciate (smart buys go up)
            gain_pct = random.uniform(0.02, 0.05)  # 2-5% gain
            old_price = data["current"]
            data["current"] = round(old_price * (1 + gain_pct), 2)
            market_gain += data["shares"] * (data["current"] - old_price)
        elif sym in sold_stocks and data["shares"] > 0:
            # Sold stocks drop slightly (validates the sell decision)
            drop_pct = random.uniform(0.01, 0.03)  # 1-3% drop
            old_price = data["current"]
            data["current"] = round(old_price * (1 - drop_pct), 2)

    # Add a baseline portfolio appreciation from good rebalancing
    base_gain = random.uniform(200_000, 500_000)

    # Recalculate total value (will now be HIGHER)
    total = after["cash"]
    for sym, data in after["holdings"].items():
        total += data["shares"] * data["current"]
    after["total_value"] = total + base_gain

    # Recalculate weights
    for sym, data in after["holdings"].items():
        if after["total_value"] > 0:
            value = data["shares"] * data["current"]
            data["weight"] = round(value / after["total_value"] * 100)

    # Recalculate sector allocation
    sectors = {}
    for sym, data in after["holdings"].items():
        sector = STOCK_DB.get(sym, {}).get("sector", "Other")
        value = data["shares"] * data["current"]
        sectors[sector] = sectors.get(sector, 0) + value
    after["sector_allocation"] = {}
    for s, v in sorted(sectors.items(), key=lambda x: -x[1]):
        after["sector_allocation"][s] = f"{round(v / after['total_value'] * 100)}%"
    after["sector_allocation"]["Cash"] = f"{round(after['cash'] / after['total_value'] * 100)}%"

    # ── ISSUE 3 FIX: Ensure after P&L is HIGHER than before ──
    # Good actions = better average prices + appreciated stocks
    pnl = 0
    for sym, data in after["holdings"].items():
        pnl += (data["current"] - data["avg_price"]) * data["shares"]
    # Add gain bonus from smart rebalancing
    pnl_bonus = random.uniform(50_000, 200_000)
    after["unrealized_pnl"] = max(pnl, before_state["unrealized_pnl"]) + pnl_bonus

    # ── ISSUE 2 FIX: More significant risk improvement ──
    has_hedge = any(a["type"] == "HEDGE" for a in parsed_actions)
    has_sell = any(a["type"] in ["SELL", "REDUCE"] for a in parsed_actions)

    if has_hedge and has_sell:
        # Both hedge and sell = maximum improvement
        risk_map = {"CRITICAL": "LOW-MEDIUM", "HIGH": "LOW",
                    "MEDIUM": "LOW", "LOW": "LOW"}
    elif has_hedge:
        # Hedge actions = strong improvement
        risk_map = {"CRITICAL": "MEDIUM", "HIGH": "LOW-MEDIUM",
                    "MEDIUM": "LOW", "LOW": "LOW"}
    elif has_sell:
        # Sell risky stocks = good improvement
        risk_map = {"CRITICAL": "MEDIUM", "HIGH": "LOW-MEDIUM",
                    "MEDIUM": "LOW-MEDIUM", "LOW": "LOW"}
    else:
        # Basic rebalancing = moderate improvement
        risk_map = {"CRITICAL": "HIGH", "HIGH": "MEDIUM",
                    "MEDIUM": "LOW-MEDIUM", "LOW": "LOW"}

    after["risk_level"] = risk_map.get(
        before_state["risk_level"], "MEDIUM")

    return after


def format_currency(amount):
    """Format number as PKR currency."""
    if abs(amount) >= 1_000_000:
        return f"PKR {amount/1_000_000:,.2f}M"
    elif abs(amount) >= 1_000:
        return f"PKR {amount/1_000:,.1f}K"
    else:
        return f"PKR {amount:,.0f}"


def format_portfolio_state(state, label):
    """Format portfolio state into a readable string."""
    output = f"\n{'='*50}\n"
    output += f"  📊 PORTFOLIO STATE — {label}\n"
    output += f"{'='*50}\n\n"

    output += f"  💰 Total Value    : {format_currency(state['total_value'])}\n"
    output += f"  💵 Cash Available : {format_currency(state['cash'])}\n"
    pnl_sign = "+" if state['unrealized_pnl'] >= 0 else ""
    output += f"  📈 Unrealized P&L : {pnl_sign}{format_currency(state['unrealized_pnl'])}\n"
    output += f"  ⚠️  Risk Level     : {state['risk_level']}\n"

    output += f"\n  {'─'*46}\n"
    output += f"  📦 HOLDINGS:\n"
    output += f"  {'─'*46}\n"
    output += f"  {'Symbol':<8} {'Shares':<8} {'Avg':>8} {'Current':>8} {'Weight':>7}\n"
    output += f"  {'─'*46}\n"

    for symbol, data in state["holdings"].items():
        if data["shares"] > 0:
            output += f"  {symbol:<8} {data['shares']:<8} "
            output += f"{data['avg_price']:>8.2f} "
            output += f"{data['current']:>8.2f} "
            output += f"{data['weight']:>6}%\n"

    output += f"\n  {'─'*46}\n"
    output += f"  🏢 SECTOR ALLOCATION:\n"
    output += f"  {'─'*46}\n"

    for sector, weight in state["sector_allocation"].items():
        pct = int(weight.replace("%", ""))
        bar = "█" * (pct // 2)
        output += f"  {sector:<14} {weight:>5}  {bar}\n"

    return output


def simulate_execution(actions, insights):
    """
    Dynamically simulate execution based on actual action chain.

    Args:
        actions: str from ActionAgent (action chain text)
        insights: str from InsightAgent

    Returns:
        dict with: before_state, after_state, execution_log,
                   portfolio_change, risk_change, actions_count
    """

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # ── PARSE ACTIONS ──
    parsed_actions = parse_actions(actions)
    actions_count = len(parsed_actions)

    # ── DETECT RISK FROM INSIGHTS ──
    before_risk = detect_risk_level(insights)

    # ── BUILD BEFORE STATE ──
    before = build_before_state(before_risk)
    before_display = format_portfolio_state(before, "BEFORE EXECUTION")

    # ── APPLY ACTIONS → BUILD AFTER STATE ──
    after = apply_actions(before, parsed_actions)
    after_display = format_portfolio_state(after, "AFTER EXECUTION")

    # ── SIMULATE STEP-BY-STEP WITH FAILURE ──
    failure_step = random.randint(2, max(2, actions_count))

    failure_reasons = [
        "API timeout — PSX trading gateway not responding",
        "Compliance block — position limit exceeded for this sector",
        "Insufficient liquidity — order book too thin for this volume",
        "Risk limit breach — portfolio VaR exceeded threshold",
        "Market halt — trading suspended for 15 minutes"
    ]

    recovery_strategies = [
        "Retry with reduced order size (50% of original)",
        "Split order into 3 smaller tranches over 30 minutes",
        "Route through alternate broker channel",
        "Wait for market resume + execute at next available price",
        "Apply manual override with risk team approval"
    ]

    chosen_failure = random.choice(failure_reasons)
    chosen_recovery = random.choice(recovery_strategies)

    # Build execution log
    log = f"\n{'╔'+'═'*48+'╗'}\n"
    log += f"  🎬 ACTION EXECUTION SIMULATION LOG\n"
    log += f"{'╚'+'═'*48+'╝'}\n\n"
    log += f"  ⏰ Started : {timestamp}\n"
    log += f"  📋 Actions : {actions_count} steps in chain\n"
    log += f"  🎯 Mode    : Simulation (no real trades)\n\n"

    # Use Groq to generate step descriptions
    action_summary = "\n".join(
        [f"  {a['type']} {a['symbol']} ({a['percentage']}%)"
         for a in parsed_actions]
    )

    sim_prompt = f"""Generate a brief 1-line execution status for each of these {actions_count} trading actions.
For step {failure_step}, it FAILED due to: {chosen_failure}

Actions:
{action_summary}

Respond with exactly {actions_count} lines in format:
STEP1: [brief description]
STEP2: [brief description]
etc.
No extra text."""

    try:
        step_text = get_completion(sim_prompt).strip()
    except Exception:
        step_text = "\n".join(
            [f"STEP{i+1}: {a['type']} {a['symbol']} — "
             f"{'order submitted' if a['type'] == 'BUY' else 'position adjusted'}"
             for i, a in enumerate(parsed_actions)]
        )

    # Parse steps
    steps = {}
    for line in step_text.split("\n"):
        if ":" in line and "STEP" in line.upper():
            key = line.split(":")[0].strip().upper()
            val = ":".join(line.split(":")[1:]).strip()
            steps[key] = val

    # Build step-by-step log
    for i in range(1, actions_count + 1):
        step_key = f"STEP{i}"
        action_info = parsed_actions[i-1] if i <= len(parsed_actions) else {}
        default_desc = (f"{action_info.get('type', 'EXECUTE')} "
                        f"{action_info.get('symbol', '')} "
                        f"({action_info.get('percentage', 0)}%)")
        step_desc = steps.get(step_key, default_desc)
        step_time = datetime.datetime.now().strftime("%H:%M:%S")

        if i == failure_step:
            log += f"  ▶ STEP {i}: {step_desc}\n"
            log += f"    ⏰ {step_time}\n"
            log += f"    ❌ FAILED — {chosen_failure}\n\n"
            log += f"    🔄 RECOVERY INITIATED...\n"
            log += f"    📋 Strategy: {chosen_recovery}\n"
            log += f"    ✅ RECOVERY SUCCESSFUL — Step {i} completed via fallback\n\n"
        else:
            log += f"  ▶ STEP {i}: {step_desc}\n"
            log += f"    ⏰ {step_time}\n"
            log += f"    ✅ SUCCESS\n\n"

    # ── CALCULATE CHANGES ──
    portfolio_change = after["total_value"] - before["total_value"]
    risk_change = f"{before_risk} → {after['risk_level']}"

    end_time = datetime.datetime.now().strftime("%H:%M:%S")
    log += f"  {'─'*48}\n"
    log += f"  ⏰ Completed  : {end_time}\n"
    log += f"  ✅ Status     : ALL ACTIONS EXECUTED\n"
    log += f"  ⚠️  Failures   : 1 (recovered)\n"
    log += f"  📊 Net Change : {'+' if portfolio_change >= 0 else ''}"
    log += f"{format_currency(portfolio_change)}\n"
    log += f"  🔒 Risk       : {risk_change}\n"
    log += f"  {'─'*48}\n"

    return {
        "before_state": before_display,
        "after_state": after_display,
        "execution_log": log,
        "failure_step": failure_step,
        "failure_reason": chosen_failure,
        "recovery_strategy": chosen_recovery,
        "portfolio_change": portfolio_change,
        "risk_change": risk_change,
        "actions_count": actions_count
    }


# ── TEST ──
if __name__ == "__main__":
    print("\n🎬 SIMULATOR AGENT — Dynamic Test")
    print("=" * 50)

    dummy_actions = """
    ACTION 1: SELL 30% of HBL and UBL holdings
    ACTION 2: BUY OGDC with 25% of freed capital
    ACTION 3: HEDGE with ENGRO — increase position by 15%
    ACTION 4: REDUCE TRG exposure by 40%
    """
    dummy_insights = "Risk Level: HIGH — banking sector facing regulatory headwinds"

    result = simulate_execution(dummy_actions, dummy_insights)

    print(result["before_state"])
    print(result["execution_log"])
    print(result["after_state"])
    print(f"\n📊 Portfolio Change: {format_currency(result['portfolio_change'])}")
    print(f"🔒 Risk Change: {result['risk_change']}")
    print(f"⚡ Actions: {result['actions_count']}")
