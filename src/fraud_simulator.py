import random
from datetime import datetime, timedelta

def inject_fraud(transactions):
    """
    FRAUD SIMULATION ENGINE (DEMO MODE)

    Injects:
    1. Repeated money mule chain (graph + temporal fraud)
    2. Sudden burst fraud (behavioral + temporal fraud)

    This is intentionally aggressive for demo purposes.
    """

    now = datetime.now()

    # =========================================================
    # 🔴 1. STRONG MONEY MULE CHAIN (REPEATED TRANSFERS)
    # user_90 → user_91 → user_92 → user_93
    # =========================================================
    mule_chain = ["user_90", "user_91", "user_92", "user_93"]

    for round_num in range(3):  # repeat transfers to amplify signal
        for i in range(len(mule_chain) - 1):
            transactions.append({
                "transaction_id": f"fraud_mule_{round_num}_{i}",
                "sender_id": mule_chain[i],
                "receiver_id": mule_chain[i + 1],
                "amount": 30000 + random.randint(10000, 20000),
                "timestamp": (
                    now - timedelta(minutes=5 * (round_num * 4 + i))
                ).isoformat(),
                "location": "Delhi",
                "merchant_category": "Transfer",
                "device_id": "fraud_device_mule"
            })

    # =========================================================
    # 🔴 2. SUDDEN BURST FRAUD (SLEEPING ACCOUNT ACTIVATION)
    # =========================================================
    burst_user = "user_99"

    for i in range(6):
        transactions.append({
            "transaction_id": f"fraud_burst_{i}",
            "sender_id": burst_user,
            "receiver_id": f"user_{random.randint(1, 20)}",
            "amount": 35000 + random.randint(10000, 25000),
            "timestamp": (now - timedelta(minutes=i)).isoformat(),
            "location": "Mumbai",
            "merchant_category": "Electronics",
            "device_id": "fraud_device_burst"
        })

    return transactions
