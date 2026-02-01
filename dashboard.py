import streamlit as st

from src.behavior_features import load_transactions, build_user_behavior
from src.anomaly_detector import detect_anomalies
from src.transaction_graph import build_transaction_graph, detect_graph_anomalies
from src.risk_engine import compute_final_risk
from src.explainability import generate_explanation

st.set_page_config(page_title="NeuroAML Dashboard", layout="wide")

st.title("🧠 NeuroAML — Fraud Detection Dashboard")

transactions = load_transactions()

behavior_profiles = build_user_behavior(transactions)
behavior_risk = detect_anomalies(behavior_profiles)

graph = build_transaction_graph(transactions)
graph_risk = detect_graph_anomalies(graph)

final_risk = compute_final_risk(behavior_risk, graph_risk)

st.subheader("🔍 Account Risk Overview")

for user in final_risk:
    risk = final_risk[user]["final_risk"]
    explanation = generate_explanation(
        user,
        behavior_risk,
        graph_risk,
        final_risk
    )

    with st.expander(f"👤 {user} | Risk: {risk}"):
        st.write("**Explanation:**")
        st.write(explanation)
