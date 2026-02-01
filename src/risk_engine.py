def compute_final_risk(behavior_risk, graph_risk, temporal_risk):
    final_scores = {}

    users = set(
        list(behavior_risk.keys()) +
        list(graph_risk.keys()) +
        list(temporal_risk.keys())
    )

    for user in users:
        score = 0

        if behavior_risk.get(user, {}).get("risk_flag") == "HIGH":
            score += 0.4

        if graph_risk.get(user) == "HIGH":
            score += 0.3

        if temporal_risk.get(user) == "HIGH":
            score += 0.3

        if score >= 0.6:
            label = "HIGH"
        elif score >= 0.3:
            label = "MEDIUM"
        else:
            label = "LOW"

        final_scores[user] = {
            "risk_score": round(score, 2),
            "final_risk": label
        }

    return final_scores
