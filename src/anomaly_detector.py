from sklearn.ensemble import IsolationForest

def detect_anomalies(behavior_profiles):
    users = []
    feature_vectors = []

    for user, profile in behavior_profiles.items():
        users.append(user)
        feature_vectors.append([
            profile["transaction_count"],
            profile["average_amount"],
            profile["max_amount"],
            profile["min_amount"]
        ])

    model = IsolationForest(
        n_estimators=100,
        contamination=0.2,
        random_state=42
    )

    predictions = model.fit_predict(feature_vectors)

    results = {}

    for i, user in enumerate(users):
        results[user] = {
            "risk_flag": "HIGH" if predictions[i] == -1 else "LOW"
        }

    return results
