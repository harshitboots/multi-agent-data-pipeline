import streamlit as st
import pandas as pd
import json
from src.observability.store import get_runs, get_spans, get_guardrail_events, get_budget, init_db
from src.observability.metrics import summary_stats, cost_trend, agent_performance_table, model_usage_breakdown, run_quality_score
from src.observability.guardrails import GuardrailEngine

st.set_page_config(
    page_title="Observability · Multi-Agent Pipeline",
    page_icon="📡",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown("""
<style>
html, body, [class*="css"], .stApp { background-color: #060910 !important; color: #e2e8f0 !important; }
header[data-testid="stHeader"] { display: none !important; }
.block-container { padding: 24px 48px !important; max-width: 100% !important; }
div[data-testid="metric-container"] {
    background: #080c14 !important; border: 0.5px solid #0f1f35 !important;
    border-radius: 12px !important; padding: 16px !important;
}
div[data-testid="stMetricValue"] { color: #00ff88 !important; font-family: monospace !important; font-size: 28px !important; }
.stTabs [data-baseweb="tab"] { font-family: monospace !important; font-size: 11px !important; color: #94a3b8 !important; }
.stTabs [aria-selected="true"] { color: #38bdf8 !important; border-bottom: 2px solid #38bdf8 !important; }
</style>
""", unsafe_allow_html=True)

init_db()

st.markdown("# Observability Dashboard")
st.markdown("Real-time traces, cost analytics, agent performance and guardrails — every run logged to SQLite.")
st.markdown("---")

tab_live, tab_history, tab_cost, tab_agents, tab_guardrails, tab_settings = st.tabs([
    "Live Monitor", "Run History", "Cost Analytics", "Agent Performance", "Guardrails Log", "Settings"
])

# ── TAB 1: LIVE MONITOR ──────────────────────────────────────────────────────
with tab_live:
    st.subheader("Last Run — Live Trace")
    runs = get_runs(limit=1)
    if not runs:
        st.info("No runs yet. Run the pipeline from the main page.")
    else:
        r = runs[0]
        c1, c2, c3, c4, c5 = st.columns(5)
        c1.metric("Run ID", r["run_id"])
        c2.metric("Total Cost", f"GBP {r['total_cost_gbp']:.5f}")
        c3.metric("Latency", f"{r['total_latency_ms']}ms")
        c4.metric("Mode", r["mode"])
        c5.metric("Status", r["status"])

        spans = get_spans(r["run_id"])
        quality = run_quality_score(r["run_id"])
        st.markdown(f"**Quality score:** {quality}%")

        if spans:
            st.markdown("#### Agent Waterfall")
            max_lat = max(s["latency_ms"] for s in spans) or 1
            for s in spans:
                bar_pct = int(s["latency_ms"] / max_lat * 100)
                status_icon = "v" if s["parse_ok"] else "X"
                timeout_icon = " [TIMEOUT]" if s["status"] == "timeout" else ""
                model_short = s["model"].split("-")[1] if "-" in s["model"] else s["model"]
                st.markdown(
                    f"`{status_icon}` **{s['agent_name']:20s}**  "
                    f"`{s['latency_ms']:>5}ms`  `GBP {s['cost_gbp']:.5f}`  "
                    f"`{model_short}`{timeout_icon}"
                )
                st.progress(bar_pct)

            st.markdown("#### Agent Inspector")
            agent_names = [s["agent_name"] for s in spans]
            selected = st.selectbox("Select agent to inspect", agent_names, key="inspector_select")
            span = next(s for s in spans if s["agent_name"] == selected)

            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"**Model:** {span['model']}")
                st.markdown(f"**Tokens in:** {span['input_tokens']}  **out:** {span['output_tokens']}")
                st.markdown(f"**Cost:** GBP {span['cost_gbp']:.5f}")
                st.markdown(f"**Latency:** {span['latency_ms']}ms")
                st.markdown(f"**Parse ok:** {'Yes' if span['parse_ok'] else 'FAILED'}")
                if span["error_message"]:
                    st.error(f"Error: {span['error_message']}")
            with col2:
                if span["system_prompt"]:
                    with st.expander("System Prompt"):
                        st.text(span["system_prompt"])
                if span["raw_response"]:
                    with st.expander("Raw Response"):
                        st.text(span["raw_response"])
                if span["parsed_output"]:
                    with st.expander("Parsed Output"):
                        st.text(span["parsed_output"])

        guardrails_fired = r.get("guardrail_events", 0)
        if guardrails_fired:
            st.warning(f"{guardrails_fired} guardrail event(s) fired in this run")

    if st.button("Refresh", key="refresh_live"):
        st.rerun()

# ── TAB 2: RUN HISTORY ───────────────────────────────────────────────────────
with tab_history:
    st.subheader("All Runs")
    runs = get_runs(limit=100)
    if not runs:
        st.info("No runs yet.")
    else:
        df_runs = pd.DataFrame(runs)
        df_runs["quality"] = [run_quality_score(r["run_id"]) for r in runs]
        df_runs["cost_gbp"] = df_runs["total_cost_gbp"].map(lambda x: f"GBP {x:.5f}")
        df_runs["latency_s"] = (df_runs["total_latency_ms"] / 1000).map(lambda x: f"{x:.1f}s")
        display_cols = ["run_id", "timestamp", "source", "mode", "cost_gbp",
                        "latency_s", "parse_failures", "guardrail_events", "quality", "status"]
        st.dataframe(df_runs[display_cols], use_container_width=True, hide_index=True)

        st.markdown("#### Inspect a run")
        run_ids = [r["run_id"] for r in runs]
        sel_run = st.selectbox("Select run", run_ids, key="history_select")
        if sel_run:
            spans = get_spans(sel_run)
            if spans:
                df_spans = pd.DataFrame(spans)
                df_spans["cost_gbp"] = df_spans["cost_gbp"].map(lambda x: f"GBP {x:.5f}")
                st.dataframe(
                    df_spans[["agent_name", "model", "input_tokens", "output_tokens",
                               "cost_gbp", "latency_ms", "status", "parse_ok"]],
                    use_container_width=True, hide_index=True
                )

# ── TAB 3: COST ANALYTICS ────────────────────────────────────────────────────
with tab_cost:
    st.subheader("Cost Analytics")
    stats = summary_stats()
    c1, c2, c3, c4, c5 = st.columns(5)
    c1.metric("Total Runs", stats["total_runs"])
    c2.metric("Total Spend", f"GBP {stats['total_cost_gbp']:.4f}")
    c3.metric("Avg Cost / Run", f"GBP {stats['avg_cost_gbp']:.4f}")
    c4.metric("Avg Latency", f"{stats['avg_latency_s']}s")
    c5.metric("Success Rate", f"{stats['success_rate_pct']}%")

    trend = cost_trend(limit=30)
    if trend:
        st.markdown("#### Cost per run over time")
        df_trend = pd.DataFrame(trend)
        st.line_chart(df_trend.set_index("timestamp")["cost_gbp"])

    model_breakdown = model_usage_breakdown()
    st.markdown("#### Model spend breakdown")
    col1, col2 = st.columns(2)
    col1.metric("Haiku total", f"GBP {model_breakdown['haiku_gbp']:.4f}")
    col2.metric("Sonnet total", f"GBP {model_breakdown['sonnet_gbp']:.4f}")
    total_model = model_breakdown["haiku_gbp"] + model_breakdown["sonnet_gbp"]
    if total_model > 0:
        haiku_pct = model_breakdown["haiku_gbp"] / total_model * 100
        st.markdown(f"Haiku: {haiku_pct:.0f}% of spend  |  Sonnet: {100 - haiku_pct:.0f}%")

    runs = get_runs(200)
    if runs:
        st.markdown("#### Cost by mode (baseline vs routed)")
        df_mode = pd.DataFrame(runs).groupby("mode")["total_cost_gbp"].agg(["sum", "mean", "count"])
        df_mode.columns = ["Total GBP", "Avg GBP", "Runs"]
        st.dataframe(df_mode, use_container_width=True)

# ── TAB 4: AGENT PERFORMANCE ─────────────────────────────────────────────────
with tab_agents:
    st.subheader("Agent Performance (last 200 runs)")
    perf = agent_performance_table()
    if not perf:
        st.info("No data yet.")
    else:
        df_perf = pd.DataFrame(perf)
        df_perf.columns = [c.replace("_", " ").title() for c in df_perf.columns]
        st.dataframe(df_perf, use_container_width=True, hide_index=True)

        st.markdown("#### Reliability by agent")
        if "Agent" in df_perf.columns and "Reliability Pct" in df_perf.columns:
            st.bar_chart(df_perf.set_index("Agent")["Reliability Pct"])

        st.markdown("#### Avg latency by agent (seconds)")
        if "Avg Latency S" in df_perf.columns:
            st.bar_chart(df_perf.set_index("Agent")["Avg Latency S"])

# ── TAB 5: GUARDRAILS LOG ────────────────────────────────────────────────────
with tab_guardrails:
    st.subheader("Guardrails Event Log")
    events = get_guardrail_events(limit=200)
    if not events:
        st.success("No guardrail events yet.")
    else:
        for e in events:
            severity = e.get("severity", "info")
            icon = {"critical": "X", "warning": "!", "info": "i"}.get(severity, "i")
            color = {"critical": "#ef4444", "warning": "#f59e0b", "info": "#38bdf8"}.get(severity, "#94a3b8")
            st.markdown(
                f'<div style="border-left:3px solid {color};padding:8px 12px;margin:4px 0;'
                f'background:#080c14;border-radius:4px;font-family:monospace;font-size:12px;">'
                f'[{icon}] <b>{e["guardrail_type"]}</b> — {e["agent_name"]} — '
                f'value={e["value"]} threshold={e["threshold"]} — action={e["action"]}'
                f'<br><span style="color:#64748b;font-size:10px;">{e["timestamp"]} · run {e["run_id"]}</span>'
                f'</div>',
                unsafe_allow_html=True
            )

# ── TAB 6: SETTINGS ──────────────────────────────────────────────────────────
with tab_settings:
    st.subheader("Guardrail Settings")
    st.markdown("Configure thresholds — changes apply to the next pipeline run.")

    with st.form("guardrail_form"):
        c1, c2 = st.columns(2)
        with c1:
            budget_cap = st.number_input("Budget cap per run (GBP)", value=0.50, step=0.05, min_value=0.01)
            agent_timeout = st.number_input("Agent timeout (seconds)", value=30, step=5, min_value=5)
            min_completeness = st.number_input("Min completeness score (%)", value=60.0, step=5.0)
        with c2:
            max_pii_rows = st.number_input("Max PII rows (0 = warn always)", value=0, step=1)
            max_parse_failures = st.number_input("Max parse failures before abort", value=3, step=1)
            anomaly_warn = st.number_input("Anomaly score warn threshold (0-10)", value=9.0, step=0.5)

        guardrails_enabled = st.checkbox("Guardrails enabled", value=True)
        submitted = st.form_submit_button("Save settings")
        if submitted:
            st.session_state["guardrail_config"] = {
                "budget_cap_gbp": budget_cap,
                "agent_timeout_s": int(agent_timeout),
                "min_completeness": min_completeness,
                "max_pii_rows": int(max_pii_rows),
                "max_parse_failures": int(max_parse_failures),
                "anomaly_score_warn": anomaly_warn,
                "enabled": guardrails_enabled,
            }
            st.success("Settings saved — will apply to next run")

    st.markdown("---")
    budget = get_budget()
    st.markdown(f"**Global spend so far:** GBP {budget['total_spent_gbp']:.4f} across {budget['run_count']} runs")
