"""
Fraud Typology Reasoning Engine
Classifies suspicious behavior into AML typologies
"""

import streamlit as st


def classify_fraud_typology(user, risk_score, G):
    """
    Determines likely fraud typology for a user
    based on risk score and transaction network.
    """

    typologies = []

    # ---------------- Smurfing ----------------
    if risk_score < 0.6 and risk_score >= 0.35:
        typologies.append({
            "type": "💸 Smurfing",
            "reason": (
                "Multiple low-to-medium risk behaviors detected, "
                "consistent with transaction structuring to avoid thresholds."
            )
        })

    # ---------------- Network-Based Analysis ----------------
    if G is not None and G.has_node(user):
        neighbors = list(G.neighbors(user))
        high_risk_neighbors = [
            n for n in neighbors
            if st.session_state.dynamic_risk.get(n, 0) >= 0.7
        ]

        # Mule Network
        if len(high_risk_neighbors) >= 2:
            typologies.append({
                "type": "🧍‍♂️ Mule Network",
                "reason": (
                    "Account is directly connected to multiple high-risk entities, "
                    "indicating possible use as a money mule."
                )
            })

        # Layering
        if len(neighbors) >= 4:
            typologies.append({
                "type": "🕸️ Layering",
                "reason": (
                    "Dense transaction connectivity detected, "
                    "suggesting attempts to obscure fund origin."
                )
            })

    # ---------------- High Risk Catch ----------------
    if risk_score >= 0.7:
        typologies.append({
            "type": "🚨 High-Risk Anomalous Activity",
            "reason": (
                "Persistent high-risk behavior observed across monitoring cycles."
            )
        })

    # ---------------- Fallback ----------------
    if not typologies:
        typologies.append({
            "type": "ℹ️ No Dominant Typology Detected",
            "reason": (
                "Account shows irregular behavior but does not strongly match "
                "known AML typologies at this stage."
            )
        })

    return typologies
