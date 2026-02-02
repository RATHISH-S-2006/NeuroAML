"""
Risk Forecasting Engine
Predicts future AML risk based on historical trends
"""

def forecast_risk(user, risk_history, horizon=3):
    """
    Forecasts future risk score for a user.

    Parameters:
    - user: account ID
    - risk_history: session_state risk history
    - horizon: number of future cycles to predict

    Returns:
    - dict with forecast score and interpretation
    """

    history = risk_history.get(user, [])

    if len(history) < 2:
        return {
            "forecast_score": None,
            "forecast_level": "INSUFFICIENT DATA",
            "interpretation": "Not enough historical data to forecast risk."
        }

    # Extract recent scores
    scores = [h["score"] for h in history[-5:]]

    # Compute average risk velocity
    deltas = [
        scores[i] - scores[i - 1]
        for i in range(1, len(scores))
    ]

    avg_velocity = sum(deltas) / len(deltas)

    # Predict future score
    current_score = scores[-1]
    forecast_score = round(
        min(current_score + avg_velocity * horizon, 1.0), 3
    )

    # Forecast level
    if forecast_score >= 0.7:
        level = "HIGH"
        interpretation = (
            "🚨 Account is likely to escalate to HIGH risk soon "
            "if current behavior persists."
        )
    elif forecast_score >= 0.35:
        level = "MEDIUM"
        interpretation = (
            "⚠️ Account shows rising risk trend and may require "
            "pre-emptive monitoring."
        )
    else:
        level = "LOW"
        interpretation = (
            "✅ Risk trajectory appears stable with no immediate "
            "escalation expected."
        )

    return {
        "forecast_score": forecast_score,
        "forecast_level": level,
        "interpretation": interpretation
    }
