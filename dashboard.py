import streamlit as st

# =====================================================
# NeuroAML Dashboard (Cloud Deployment Version)
# =====================================================

from src.behavior_features import load_transactions, build_user_behavior
from src.anomaly_detector import detect_anomalies
from src.transaction_graph import build_transaction_graph, detect_graph_anomalies
from src.temporal_detector import detect_temporal_anomalies
from src.risk_engine import compute_final_risk
from src.explainability import generate_explanation

# -----------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="NeuroAML Dashboard",
    layout="wide"
)

st.title("🧠 NeuroAML — Fraud Detection Dashboard")
st.markdown(
    """
    This dashboard demonstrates an **end-to-end Anti–Money Laundering (AML) system**
    combining **behavioral analytics, transaction network analysis, and temporal intelligence**.
    """
)

# -----------------------------------------------------
# Load & Process Transactions
# -----------------------------------------------------
with st.spinner("Loading transactions and computing risk scores..."):
    transactions = load_transactions()

    # Behavioral Risk
    behavior_profiles = build_user_behavior(transactions)
    behavior_risk = detect_anomalies(behavior_profiles)

    # Graph Risk
    graph = build_transaction_graph(transactions)
    graph_risk = detect_graph_anomalies(graph)

    # Temporal Risk
    temporal_risk = detect_temporal_anomalies(transactions)

    # Final Hybrid Risk
    final_risk = compute_final_risk(
        behavior_risk,
        graph_risk,
        temporal_risk
    )

st.success("Risk analysis completed successfully.")

# -----------------------------------------------------
# Dashboard View
# -----------------------------------------------------
st.subheader("🔍 Account Risk Overview")

if not final_risk:
    st.warning("No risk data available.")
else:
    for user, result in final_risk.items():
        risk_label = result["final_risk"]
        risk_score = result["risk_score"]

        explanation = generate_explanation(
            user,
            behavior_risk,
            graph_risk,
            final_risk,
            temporal_risk
        )

        # Color coding for risk
        if risk_label == "HIGH":
            badge = "🔴 HIGH RISK"
        elif risk_label == "MEDIUM":
            badge = "🟠 MEDIUM RISK"
        else:
            badge = "🟢 LOW RISK"

        with st.expander(f"👤 {user} | {badge} | Score: {risk_score}"):
            st.markdown("**Risk Explanation:**")
            st.write(explanation)

# -----------------------------------------------------
# Footer
# -----------------------------------------------------
st.markdown("---")
st.caption(
    "NeuroAML • Behavioral + Graph + Temporal Fraud Detection • Deployed on Cloud"
)
