from fastapi import APIRouter

from src.behavior_features import load_transactions, build_user_behavior
from src.anomaly_detector import detect_anomalies
from src.transaction_graph import build_transaction_graph, detect_graph_anomalies
from src.temporal_detector import detect_temporal_anomalies
from src.risk_engine import compute_final_risk
from src.explainability import generate_explanation
from src.fraud_simulator import inject_fraud

router = APIRouter(prefix="/aml", tags=["AML"])

# 🔥 Toggle fraud simulation here
SIMULATE_FRAUD = True


def run_aml_pipeline():
    transactions = load_transactions()

    if SIMULATE_FRAUD:
        transactions = inject_fraud(transactions)

    behavior_profiles = build_user_behavior(transactions)
    behavior_risk = detect_anomalies(behavior_profiles)

    graph = build_transaction_graph(transactions)
    graph_risk = detect_graph_anomalies(graph)

    temporal_risk = detect_temporal_anomalies(transactions)

    final_risk = compute_final_risk(
        behavior_risk,
        graph_risk,
        temporal_risk
    )

    return behavior_risk, graph_risk, final_risk


@router.get("/risk-report")
def risk_report():
    _, _, final_risk = run_aml_pipeline()
    return final_risk


@router.get("/explain/{user_id}")
def explain_user(user_id: str):
    behavior_risk, graph_risk, final_risk = run_aml_pipeline()

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
