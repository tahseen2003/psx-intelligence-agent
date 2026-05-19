# =====================================================
#  📈 STREAMLIT UI — PSX Intelligence Dashboard
#  Premium Glassmorphism dark-themed Pakistan Stock Exchange Agent
# =====================================================

import streamlit as st
from orchestrator import AntigravityOrchestrator

# ── PAGE CONFIG ──
st.set_page_config(
    page_title="PSX Intelligence Dashboard",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ── CUSTOM CSS ──
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;600;700&display=swap');

    /* Global */
    .stApp {
        background: radial-gradient(circle at top right, #131422, #08090f);
        color: #e2e8f0;
        font-family: 'Outfit', sans-serif;
    }
    
    /* Headers */
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif !important;
        color: #f8fafc;
        font-weight: 600;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: rgba(15, 23, 42, 0.4) !important;
        backdrop-filter: blur(12px) !important;
        border-right: 1px solid rgba(255, 255, 255, 0.05);
    }
    
    /* Hero Title */
    .hero-title {
        font-size: 3rem;
        font-weight: 700;
        background: linear-gradient(135deg, #3b82f6, #8b5cf6, #ec4899);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    
    .hero-sub {
        font-size: 1.1rem;
        color: #94a3b8;
        margin-bottom: 2rem;
    }
    
    /* Glassmorphism Cards */
    .glass-card {
        background: rgba(30, 41, 59, 0.3);
        backdrop-filter: blur(10px);
        -webkit-backdrop-filter: blur(10px);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 16px;
        padding: 24px;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.1);
        margin-bottom: 1.5rem;
        transition: transform 0.3s ease, border-color 0.3s ease;
    }
    
    .glass-card:hover {
        transform: translateY(-2px);
        border-color: rgba(139, 92, 246, 0.5);
    }
    
    /* KPIs */
    .kpi-container {
        display: flex;
        flex-direction: column;
        align-items: center;
        justify-content: center;
    }
    .kpi-value {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #fff, #94a3b8);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    .kpi-value.positive { background: linear-gradient(135deg, #34d399, #059669); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .kpi-value.negative { background: linear-gradient(135deg, #f87171, #dc2626); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
    .kpi-label {
        font-size: 0.875rem;
        color: #cbd5e1;
        text-transform: uppercase;
        letter-spacing: 1.5px;
        margin-top: 0.5rem;
        text-align: center;
    }
    
    /* Buttons */
    .stButton>button {
        border-radius: 8px !important;
        font-weight: 600 !important;
        transition: all 0.3s ease !important;
        background: linear-gradient(135deg, #4f46e5, #7c3aed) !important;
        border: none !important;
        color: white !important;
    }
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 10px 20px -10px rgba(124, 58, 237, 0.5) !important;
    }
    
    /* Divider */
    hr {
        border-color: rgba(255, 255, 255, 0.05);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)


# ── MAIN LAYOUT ──
st.markdown('<div class="hero-title">📈 PSX Intelligence Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="hero-sub">Content → Insight → Action | Powered by Antigravity Agents</div>', unsafe_allow_html=True)


# ── SIDEBAR (INPUTS) ──
with st.sidebar:
    st.markdown("### 📥 Data Sources")
    st.caption("Configure your inputs for the PSX Agent Pipeline.")
    
    input_method = st.radio(
        "Input Method:",
        ["📁 Sample PSX Data", "📤 Upload Files", "✏️ Paste Text"],
        label_visibility="collapsed"
    )
    
    source_texts = []
    source_list = []
    sources_ready = False
    
    if input_method == "📁 Sample PSX Data":
        st.info("Using built-in PSX sources:\n- Market Report\n- Stock Data CSV\n- News Article")
        source_list = [
            "data/psx_market_report.txt",
            "data/psx_news_article.txt",
            "data/psx_stock_data.csv"
        ]
        sources_ready = True
        
    elif input_method == "📤 Upload Files":
        st.markdown("Upload files (TXT, CSV, JSON):")
        uploaded_files = st.file_uploader("Upload", accept_multiple_files=True, type=['txt', 'csv', 'json'], label_visibility="collapsed")
        
        if uploaded_files:
            import os
            os.makedirs("data", exist_ok=True)
            for f in uploaded_files:
                path = f"data/{f.name}"
                with open(path, "wb") as out:
                    out.write(f.getbuffer())
                source_list.append(path)
            sources_ready = True
            st.success(f"{len(source_list)} files uploaded.")
            
    else:
        user_text = st.text_area("Paste market report/data:", height=200)
        if user_text and len(user_text.strip()) > 10:
            import os
            os.makedirs("data", exist_ok=True)
            with open("data/user_input.txt", "w", encoding="utf-8") as f:
                f.write(user_text)
            source_list.append("data/user_input.txt")
            sources_ready = True

    st.markdown("---")
    st.markdown("### ⚙️ Pipeline Settings")
    st.caption("Customize agent behavior")
    risk_tolerance = st.select_slider("Risk Tolerance", options=["Low", "Medium", "High"], value="Medium")
    
    run_button = st.button("🚀 Execute Agents", use_container_width=True, disabled=not sources_ready)


# ── MAIN CANVAS (RESULTS & PIPELINE) ──

if not sources_ready and not run_button:
    st.markdown("""
    <div class="glass-card" style="text-align: center; padding: 4rem 2rem;">
        <h2 style="color: #94a3b8; font-weight: 400;">Awaiting Data Sources</h2>
        <p style="color: #64748b;">Please select or provide data sources from the sidebar to begin the analysis.</p>
    </div>
    """, unsafe_allow_html=True)

if run_button:
    st.markdown("### 🔄 Agent Execution Trace")
    
    # Run the pipeline with st.status
    orchestrator = AntigravityOrchestrator()
    
    try:
        with st.status("Initializing PSX Agentic Pipeline...", expanded=True) as status:
            
            st.write("📄 **ReaderAgent**: Ingesting raw data sources...")
            from reader_agent import read_all_sources
            sources_data = read_all_sources(source_list)
            st.write(f"✅ Loaded {len(sources_data)} sources.")
            
            st.write("🔍 **InsightAgent**: Extracting financial metrics via Groq...")
            from insight_agent import extract_insights
            insights = extract_insights(sources_data)
            st.write("✅ Insights formulated.")
            
            st.write("⚖️ **ContradictionAgent**: Cross-referencing points...")
            from contradiction_agent import detect_contradictions
            contradictions = detect_contradictions(sources_data)
            st.write("⚠️ Fact-check complete.")
            
            st.write("⚡ **ActionAgent**: Synthesizing action chain...")
            from action_agent import generate_actions
            actions = generate_actions(insights, contradictions)
            st.write("✅ Actions determined.")
            
            st.write("🎬 **SimulatorAgent**: Executing simulated trades...")
            from simulator_agent import simulate_execution
            simulation = simulate_execution(actions, insights)
            st.write("✅ Simulation finished.")
            
            status.update(label="Pipeline Execution Complete!", state="complete", expanded=False)
            
        st.success("Analysis successfully generated.")
        
        # ── KPI DASHBOARD ──
        st.markdown("### 📊 Portfolio Impact Simulation")
        
        pchange = simulation["portfolio_change"]
        pchange_sign = "+" if pchange >= 0 else ""
        if abs(pchange) >= 1_000_000:
            pchange_display = f"{pchange_sign}PKR {pchange/1_000_000:.2f}M"
        else:
            pchange_display = f"{pchange_sign}PKR {pchange/1_000:,.0f}K"
            
        pchange_class = "positive" if pchange >= 0 else "negative"
        
        st.markdown(f"""
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1.5rem; margin-bottom: 2rem;">
            <div class="glass-card kpi-container">
                <div class="kpi-value {pchange_class}">{pchange_display}</div>
                <div class="kpi-label">Simulated Returns</div>
            </div>
            <div class="glass-card kpi-container">
                <div class="kpi-value">{simulation['risk_change']}</div>
                <div class="kpi-label">Risk Profile Shift</div>
            </div>
            <div class="glass-card kpi-container">
                <div class="kpi-value">{len(sources_data)}</div>
                <div class="kpi-label">Sources Processed</div>
            </div>
            <div class="glass-card kpi-container">
                <div class="kpi-value">{simulation['actions_count']}</div>
                <div class="kpi-label">Actions Synthesized</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # ── DETAILED RESULTS TABS ──
        st.markdown("### 📑 Detailed Analysis")
        
        tab1, tab2, tab3, tab4 = st.tabs(["💡 Insights", "⚡ Recommended Actions", "⚖️ Fact-Check", "🎬 Simulation Log"])
        
        with tab1:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(insights)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab2:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.markdown(actions)
            st.markdown('</div>', unsafe_allow_html=True)
            
        with tab3:
            if "No contradictions" in contradictions:
                st.success("No contradictions found in the sources.")
            else:
                st.warning("Potential contradictions detected.")
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown(contradictions)
                st.markdown('</div>', unsafe_allow_html=True)
                
        with tab4:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown("**Initial State**")
                st.code(simulation["before_state"], language="json")
            with col2:
                st.markdown("**Final State**")
                st.code(simulation["after_state"], language="json")
            
            st.markdown("**Execution Log**")
            st.code(simulation["execution_log"], language="text")
            
            if simulation['failure_step'] != "None":
                st.error(f"⚠️ Simulated Error at step {simulation['failure_step']}: {simulation['failure_reason']}")
                st.success(f"🛠️ Agent Recovery: {simulation['recovery_strategy']}")
            st.markdown('</div>', unsafe_allow_html=True)
            
        st.balloons()
        
    except Exception as e:
        st.error(f"An error occurred during execution: {e}")
