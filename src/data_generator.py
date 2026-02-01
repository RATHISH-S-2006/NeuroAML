import random
import uuid
from datetime import datetime, timedelta

# Generate a single fake transaction
def generate_transaction():
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "sender_id": f"user_{random.randint(1, 50)}",
        "receiver_id": f"user_{random.randint(1, 50)}",
        "amount": round(random.uniform(100, 10000), 2),
        "timestamp": datetime.now().isoformat(),
        "location": random.choice(["Chennai", "Bangalore", "Mumbai", "Delhi"]),
        "merchant_category": random.choice([
            "Groceries", "Electronics", "Fuel", "Shopping", "Food"
        ]),
        "device_id": f"device_{random.randint(1, 20)}"
    }
    return transaction


# Generate multiple transactions
def generate_transactions(count=10):
    return [generate_transaction() for _ in range(count)]
