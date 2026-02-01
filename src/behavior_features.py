import csv
from collections import defaultdict

FILE_PATH = "data/transactions.csv"

def load_transactions():
    with open(FILE_PATH, newline="") as file:
        reader = csv.DictReader(file)
        return list(reader)

def build_user_behavior(transactions):
    user_data = defaultdict(list)

    for tx in transactions:
        user_data[tx["sender_id"]].append(float(tx["amount"]))

    behavior_profiles = {}

    for user, amounts in user_data.items():
        behavior_profiles[user] = {
            "transaction_count": len(amounts),
            "average_amount": round(sum(amounts) / len(amounts), 2),
            "max_amount": max(amounts),
            "min_amount": min(amounts)
        }

    return behavior_profiles
