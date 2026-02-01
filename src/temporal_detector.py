from collections import defaultdict
from datetime import datetime

def detect_temporal_anomalies(transactions):
    user_transactions = defaultdict(list)

    # Group transactions by sender
    for tx in transactions:
        user = tx["sender_id"]
        amount = float(tx["amount"])
        timestamp = datetime.fromisoformat(tx["timestamp"])

        user_transactions[user].append((timestamp, amount))

    temporal_risk = {}

    for user, txs in user_transactions.items():
        # Sort by time
        txs.sort(key=lambda x: x[0])

        amounts = [amt for _, amt in txs]

        if len(amounts) < 3:
            temporal_risk[user] = "LOW"
            continue

        avg_early = sum(amounts[:len(amounts)//2]) / (len(amounts)//2)
        avg_late = sum(amounts[len(amounts)//2:]) / (len(amounts)//2)

        if avg_late > avg_early * 2:
            temporal_risk[user] = "HIGH"
        else:
            temporal_risk[user] = "LOW"

    return temporal_risk
