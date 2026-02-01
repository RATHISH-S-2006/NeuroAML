from fastapi import FastAPI

from src.behavior_features import load_transactions, build_user_behavior
from src.anomaly_detector import detect_anomalies
from src.transaction_graph import build_transaction_graph, detect_graph_anomalies
from src.risk_engine import compute_final_risk
from src.explainability import generate_explanation

app = FastAPI(title="NeuroAML API")

def run_engine():
    transactions = load_transactions()

    behavior_profiles = build_user_behavior(transactions)
    behavior_risk = detect_anomalies(behavior_profiles)

    graph = build_transaction_graph(transactions)
    graph_risk = detect_graph_anomalies(graph)

    final_risk = compute_final_risk(behavior_risk, graph_risk)

    return behavior_risk, graph_risk, final_risk

@app.get("/risk-report")
def risk_report():
    _, _, final_risk = run_engine()
    return final_risk

@app.get("/explain/{user_id}")
def explain_user(user_id: str):
    behavior_risk, graph_risk, final_risk = run_engine()

    explanation = generate_explanation(
        user_id,
        behavior_risk,
        graph_risk,
        final_risk
    )

    return {
        "user": user_id,
        "risk": final_risk.get(user_id, {}),
        "explanation": explanation
    }
