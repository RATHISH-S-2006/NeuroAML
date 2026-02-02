from fastapi import FastAPI

from src.behavior_features import load_transactions, build_user_behavior
from src.anomaly_detector import detect_anomalies
from src.transaction_graph import build_transaction_graph, detect_graph_anomalies
from src.temporal_detector import detect_temporal_anomalies
from src.risk_engine import compute_final_risk
from src.explainability import generate_explanation
from src.fraud_simulator import inject_fraud

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

    results = {}

    for user, result in final_risk.items():
        explanation = generate_explanation(
            user,
            behavior_risk,
            graph_risk,
            final_risk
        )

        results[user] = {
            "risk": result,
            "explanation": explanation
        }

    return results


# -------------------------------------------------
# FastAPI App (CORRECTED)
# -------------------------------------------------

app = FastAPI(
    title="NeuroAML API",
    description="Multi-layer Anti–Money Laundering Intelligence System",
    version="1.0.0"
)


@app.get("/")
def health_check():
    return {"status": "NeuroAML API is running"}


@app.get("/aml/run")
def run_aml():
    return run_aml_pipeline()
