def generate_explanation(user, behavior_risk, graph_risk, final_risk, temporal_risk=None):
    explanations = []

    if behavior_risk.get(user, {}).get("risk_flag") == "HIGH":
        explanations.append(
            "The account shows abnormal transaction behavior compared to typical users."
        )

    if graph_risk.get(user) == "HIGH":
        explanations.append(
            "The account is part of a suspicious transaction network indicating possible money mule activity."
        )

    if temporal_risk and temporal_risk.get(user) == "HIGH":
        explanations.append(
            "The account shows a sudden escalation in transaction amounts over a short time period."
        )

    if final_risk[user]["final_risk"] == "HIGH":
        explanations.append(
            "Based on combined behavioral, network, and temporal indicators, this account is classified as high risk."
        )

    if not explanations:
        explanations.append(
            "The account shows normal behavior with no significant risk indicators."
        )

    return " ".join(explanations)
