import networkx as nx

def build_transaction_graph(transactions):
    G = nx.DiGraph()

    for tx in transactions:
        sender = tx["sender_id"]
        receiver = tx["receiver_id"]
        amount = float(tx["amount"])

        G.add_edge(sender, receiver, amount=amount)

    return G


def detect_graph_anomalies(G):
    risk_scores = {}

    degree_centrality = nx.degree_centrality(G)

    for node, score in degree_centrality.items():
        if score > 0.2:
            risk_scores[node] = "HIGH"
        else:
            risk_scores[node] = "LOW"

    return risk_scores
