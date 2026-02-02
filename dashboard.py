import networkx as nx
import streamlit as st
import requests
import pandas as pd
import time
from datetime import datetime
import random
import matplotlib.pyplot as plt
from intelligence.typology_engine import classify_fraud_typology
from intelligence.risk_forecast import forecast_risk

from phase4 import (
    aml_compliance_mapping,
    compute_impact_metrics,
    demo_mode_multiplier,
    demo_mode_toggle_ui
)

from governance.case_management import (
    create_case,
    update_case_status,
    get_cases,
    get_audit_trail
)

from governance.sar_export import (
    generate_sar_payload,
    export_sar_as_json
)

# =====================================================
# NEUROAML — REAL-TIME AML COMMAND CENTER (PHASE 2)
# =====================================================

# -----------------------------------------------------
# Page Config
# -----------------------------------------------------
st.set_page_config(
    page_title="NeuroAML | Real-Time AML Command Center",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -----------------------------------------------------
# Constants
# -----------------------------------------------------
API_URL = "http://127.0.0.1:8000/aml/run"
AUTO_REFRESH_SECONDS = 5

# -----------------------------------------------------
# Session State Initialization
# -----------------------------------------------------
if "dynamic_risk" not in st.session_state:
    st.session_state.dynamic_risk = {}

if "risk_history" not in st.session_state:
    st.session_state.risk_history = {}

if "escalated_accounts" not in st.session_state:
    st.session_state.escalated_accounts = set()

if "alert_log" not in st.session_state:
    st.session_state.alert_log = []

if "mode" not in st.session_state:
    st.session_state.mode = "🛰️ Monitoring"

if "last_refresh" not in st.session_state:
    st.session_state.last_refresh = datetime.now()

# -----------------------------------------------------
# Helper Functions
# -----------------------------------------------------
def fetch_backend_data():
    r = requests.get(API_URL, timeout=5)
    r.raise_for_status()
    return r.json()

def record_risk_history(user, score):
    if user not in st.session_state.risk_history:
        st.session_state.risk_history[user] = []
    st.session_state.risk_history[user].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "score": score
    })

def log_alert(message):
    ts = datetime.now().strftime("%H:%M:%S")
    st.session_state.alert_log.insert(0, f"[{ts}] {message}")
    st.session_state.alert_log = st.session_state.alert_log[:10]

# -----------------------------------------------------
# 🔥 Dynamic Explanation Engine (ADDED)
# -----------------------------------------------------
def generate_dynamic_explanation(user, score, level, G):
    if G is None or not G.has_node(user):
        neighbors = []
    else:
        neighbors = list(G.neighbors(user))

    high_risk_neighbors = [
        n for n in neighbors
        if st.session_state.dynamic_risk.get(n, 0) >= 0.7
    ]

    if level == "HIGH":
        return (
            "🚨 The account shows persistent high-risk behavior with rapid risk "
            "escalation over time. Transactional exposure to other high-risk "
            "accounts suggests potential money laundering, layering, or "
            "mule-network activity."
        )

    if level == "MEDIUM":
        if high_risk_neighbors:
            return (
                "⚠️ The account displays suspicious behavior and is directly "
                "connected to one or more high-risk accounts, indicating possible "
                "risk propagation or early-stage laundering."
            )
        return (
            "⚠️ Abnormal transaction patterns detected compared to baseline users. "
            "Enhanced monitoring and due diligence are advised."
        )

    return (
        "✅ The account currently shows normal transaction behavior with no "
        "significant laundering indicators. It remains under continuous monitoring."
    )

# -----------------------------------------------------
# 🔥 Dynamic Status Engine (ADDED)
# -----------------------------------------------------
def determine_dynamic_status(user, score, level):
    history = st.session_state.risk_history.get(user, [])

    if level == "HIGH":
        return "🚨 Escalated"

    if level == "MEDIUM":
        if len(history) >= 3:
            return "🕵️ Under Review"
        return "⚠️ Watchlisted"

    return "🟢 Monitoring"

# -----------------------------------------------------
# Transaction Network Engine (Phase 3)
# -----------------------------------------------------
def build_transaction_network(users, max_edges=120):
    G = nx.Graph()

    for user in users:
        risk = st.session_state.dynamic_risk.get(user, 0)
        G.add_node(user, risk=risk)

    for _ in range(max_edges):
        u1, u2 = random.sample(users, 2)
        amount = random.randint(1000, 50000)
        G.add_edge(u1, u2, amount=amount)

    return G

# -----------------------------------------------------
# Network Visualization (Phase 3.2)
# -----------------------------------------------------
def draw_transaction_network(G, focus_user=None):
    plt.figure(figsize=(10, 8))
    pos = nx.spring_layout(G, seed=42, k=0.35)

    node_colors = []
    node_sizes = []

    for node in G.nodes():
        risk = st.session_state.dynamic_risk.get(node, 0)

        if node == focus_user:
            node_colors.append("red")
            node_sizes.append(900)
        elif focus_user and node in G.neighbors(focus_user):
            node_colors.append("orange")
            node_sizes.append(600)
        else:
            if risk >= 0.7:
                node_colors.append("#7f1d1d")
            elif risk >= 0.35:
                node_colors.append("#78350f")
            else:
                node_colors.append("#14532d")
            node_sizes.append(300)

    nx.draw(
        G, pos,
        node_color=node_colors,
        node_size=node_sizes,
        edge_color="#374151",
        alpha=0.9,
        with_labels=False
    )

    if focus_user:
        labels = {n: n for n in [focus_user] + list(G.neighbors(focus_user))}
        nx.draw_networkx_labels(G, pos, labels, font_size=9)

    plt.title("🕸️ Transaction Money Flow Network", fontsize=14)
    plt.axis("off")
    st.pyplot(plt)
    plt.close()

# -----------------------------------------------------
# Sidebar — Controls
# -----------------------------------------------------
demo_mode_toggle_ui()
st.sidebar.markdown("## 🧠 NeuroAML")
st.sidebar.caption("Real-Time AML Command Center")

st.session_state.mode = st.sidebar.radio(
    "Operation Mode",
    ["🛰️ Monitoring", "🕵️ Investigation", "🧾 Case Dashboard", "🧪 Simulation"]
)

auto_refresh = st.sidebar.checkbox("🔄 Auto Refresh", value=True)
st.sidebar.caption(f"Last Refresh: {st.session_state.last_refresh.strftime('%H:%M:%S')}")

# -----------------------------------------------------
# Evidence & Intelligence Narrative (Phase 3.3)
# -----------------------------------------------------
def generate_evidence_report(user, G):
    evidence = []

    history = st.session_state.risk_history.get(user, [])
    if len(history) >= 2:
        delta = round(history[-1]["score"] - history[0]["score"], 2)
        if delta > 0.3:
            evidence.append(
                f"📈 Rapid risk escalation detected (Δ score = {delta})."
            )

    neighbors = list(G.neighbors(user))
    high_risk_neighbors = [
        n for n in neighbors
        if st.session_state.dynamic_risk.get(n, 0) >= 0.7
    ]

    if high_risk_neighbors:
        evidence.append(
            f"🔗 Direct links to HIGH-RISK accounts: {', '.join(high_risk_neighbors)}"
        )

    if len(neighbors) >= 3:
        evidence.append(
            "🕸️ Dense transaction connectivity suggests layering or mule activity."
        )

    if user in st.session_state.escalated_accounts:
        evidence.append(
            "🚨 Account remains in HIGH-RISK state across multiple cycles."
        )

    if not evidence:
        evidence.append("ℹ️ No strong laundering indicators beyond baseline anomaly.")

    return evidence

# -----------------------------------------------------
# AML Compliance Mapping (Phase 4.1)
# -----------------------------------------------------
def aml_compliance_mapping(user, level):
    if level == "HIGH":
        return [
            "FATF Recommendation 10: Customer Due Diligence failure",
            "FATF Recommendation 11: Suspicious transaction patterns detected",
            "Layering & Mule Network typology indicators present"
        ]

    if level == "MEDIUM":
        return [
            "Early warning indicators under FATF Recommendation 20",
            "Unusual transaction behavior requiring enhanced monitoring"
        ]

    return [
        "No immediate AML compliance violations detected"
    ]


# -----------------------------------------------------
# Auto Refresh Logic
# -----------------------------------------------------
if auto_refresh:
    time.sleep(AUTO_REFRESH_SECONDS)
    st.session_state.last_refresh = datetime.now()
    st.rerun()

# -----------------------------------------------------
# Header
# -----------------------------------------------------
st.markdown("""
# 🧠 NeuroAML — Real-Time Financial Crime Command Center
**Live monitoring of behavioral, network, and temporal fraud intelligence**
""")

# -----------------------------------------------------
# Fetch Backend Data
# -----------------------------------------------------
with st.spinner("📡 Synchronizing with AML backend..."):
    raw_data = fetch_backend_data()

# -----------------------------------------------------
# Dynamic Risk Evolution Engine
# -----------------------------------------------------
rows = []

for user, payload in raw_data.items():
    base_score = payload["risk"]["risk_score"]

    if user not in st.session_state.dynamic_risk:
        st.session_state.dynamic_risk[user] = base_score

    drift = random.uniform(0.01, 0.05) * demo_mode_multiplier()
    if st.session_state.dynamic_risk[user] >= 0.6:
        drift *= 1.5
    elif st.session_state.dynamic_risk[user] >= 0.3:
        drift *= 1.2

    st.session_state.dynamic_risk[user] = min(
        st.session_state.dynamic_risk[user] + drift, 1.0
    )

    score = round(st.session_state.dynamic_risk[user], 3)

    if score >= 0.7:
        level = "HIGH"
        if user not in st.session_state.escalated_accounts:
            log_alert(f"🚨 Risk escalated to HIGH for {user}")
        st.session_state.escalated_accounts.add(user)
    elif score >= 0.35:
        level = "MEDIUM"
    else:
        level = "LOW"

    record_risk_history(user, score)

    rows.append({
        "User": user,
        "Risk Score": score,
        "Risk Level": level,
        "Explanation": generate_dynamic_explanation(
            user, score, level,
            st.session_state.get("tx_graph")
        ),
        "Status": determine_dynamic_status(user, score, level)
    })

df = pd.DataFrame(rows)

# Build / update transaction network (SAFE UPDATE)
current_users = df["User"].tolist()

if "tx_graph" not in st.session_state:
    st.session_state.tx_graph = build_transaction_network(current_users)
else:
    G = st.session_state.tx_graph
    for u in current_users:
        if not G.has_node(u):
            G.add_node(u, risk=st.session_state.dynamic_risk.get(u, 0))


# -----------------------------------------------------
# Metrics
# -----------------------------------------------------
total_users = len(df)
high = (df["Risk Level"] == "HIGH").sum()
medium = (df["Risk Level"] == "MEDIUM").sum()
low = (df["Risk Level"] == "LOW").sum()

# =====================================================
# 🛰️ MODE 1 — MONITORING
# =====================================================
if st.session_state.mode == "🛰️ Monitoring":

    st.markdown("## 🛰️ Live System Monitoring")

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("👥 Accounts", total_users)
    c2.metric("🔴 High Risk", high)
    c3.metric("🟠 Medium Risk", medium)
    c4.metric("🟢 Low Risk", low)

    st.markdown("### 📊 System Impact Metrics")
    impact = compute_impact_metrics(df, st.session_state.risk_history)
    for k, v in impact.items():
        st.write(f"**{k}:** {v}")

    st.markdown("### 🚨 Live Alert Feed")
    if st.session_state.alert_log:
        for alert in st.session_state.alert_log:
            st.error(alert)
    else:
        st.success("No critical alerts detected.")

    st.markdown("### 📊 Risk Overview")

    def color_risk(val):
        if val == "HIGH":
            return "background-color:#7f1d1d"
        elif val == "MEDIUM":
            return "background-color:#78350f"
        return "background-color:#14532d"

    st.dataframe(
        df.style.applymap(color_risk, subset=["Risk Level"]),
        use_container_width=True,
        height=420
    )

# =====================================================
# 🕵️ MODE 2 — INVESTIGATION
# =====================================================
elif st.session_state.mode == "🕵️ Investigation":

    st.markdown("## 🕵️ Investigation Console")

    suspects = df[df["Risk Level"] != "LOW"]

    if suspects.empty:
        st.info("No accounts under investigation.")
    else:
        user = st.selectbox("Select Account", suspects["User"])
        record = suspects[suspects["User"] == user].iloc[0]

        st.markdown(f"""
        ### 🔍 Account `{user}`
        **Risk Level:** {record["Risk Level"]}  
        **Current Risk Score:** {record["Risk Score"]}
        """)

        st.markdown("#### ⏱️ Risk Evolution Timeline")
        hist_df = pd.DataFrame(st.session_state.risk_history[user])
        st.line_chart(hist_df.set_index("time")["score"])

        st.markdown("---")

        st.markdown("#### 🕸️ Money Flow Network")
        draw_transaction_network(st.session_state.tx_graph, focus_user=user)

        st.markdown("#### 🔗 Connected Accounts")
        for n in st.session_state.tx_graph.neighbors(user):
            r = st.session_state.dynamic_risk.get(n, 0)
            badge = "🔴 HIGH" if r >= 0.7 else "🟠 MEDIUM" if r >= 0.35 else "🟢 LOW"
            st.write(f"• `{n}` — Risk Score: `{round(r,2)}` {badge}")

        st.markdown("#### 🧠 Intelligence Narrative")
        st.write(record["Explanation"])

        st.markdown("#### 🧾 Evidence Chain")
        for i, e in enumerate(generate_evidence_report(user, st.session_state.tx_graph), 1):
            st.markdown(f"**Evidence {i}:** {e}")

                # ---------------- Fraud Typology Classification ----------------
        st.markdown("#### 🧠 Fraud Typology Assessment")

        typologies = classify_fraud_typology(
            user=user,
            risk_score=record["Risk Score"],
            G=st.session_state.tx_graph
        )

        for t in typologies:
            st.write(f"**{t['type']}** — {t['reason']}")

        # ---------------- Risk Forecasting ----------------
        st.markdown("#### 🔮 Risk Forecast (Early Warning)")

        forecast = forecast_risk(
            user=user,
            risk_history=st.session_state.risk_history,
            horizon=3
        )

        if forecast["forecast_score"] is not None:
            st.write(
                f"**Predicted Risk Score:** {forecast['forecast_score']} "
                f"({forecast['forecast_level']})"
            )
            st.write(forecast["interpretation"])
        else:
            st.info(forecast["interpretation"])


        st.markdown("#### ⚖️ System Verdict")
        if record["Risk Level"] == "HIGH":
            st.error("🚨 High confidence laundering threat. Immediate escalation recommended.")
        elif record["Risk Level"] == "MEDIUM":
            st.warning("⚠️ Suspicious behavior detected. Enhanced monitoring advised.")
        else:
            st.success("✅ No critical laundering threat detected.")

        st.markdown("#### 📜 AML Compliance Mapping")

        for rule in aml_compliance_mapping(user, record["Risk Level"]):
            st.write(f"• {rule}")

        # ---------------- Case Management ----------------
        st.markdown("#### 🧾 Case Management")

        case = create_case(user, record["Risk Level"])

        st.write(f"**Case ID:** {case['case_id']}")
        st.write(f"**Current Status:** {case['status']}")

        c1, c2, c3 = st.columns(3)

        if c1.button("🕵️ Mark Under Review"):
            update_case_status(case["case_id"], "🕵️ Under Review", "Analyst reviewing case")

        if c2.button("🚨 Escalate Case"):
            update_case_status(case["case_id"], "🚨 Escalated", "High risk confirmed")

        if c3.button("✅ Close Case"):
            update_case_status(case["case_id"], "✅ Closed", "False positive or resolved")

        st.markdown("#### 🧾 Audit Trail")

        audit = get_audit_trail(case["case_id"])

        if audit:
            for a in audit:
                st.write(f"[{a['time']}] {a['message']}")
        else:
            st.info("No actions recorded yet.")

        # ---------------- SAR Report Export ----------------

        st.markdown("#### 📤 SAR Report Export")

        # ✅ Always fetch case safely
        case = create_case(user, record["Risk Level"])

        if st.button("📄 Generate SAR Report"):
            sar_payload = generate_sar_payload(
                case=case,
                evidence=generate_evidence_report(
                    user,
                    st.session_state.tx_graph
                ),
                typologies=classify_fraud_typology(
                    user,
                    record["Risk Score"],
                    st.session_state.tx_graph
                ),
                forecast=forecast,
                compliance_rules=aml_compliance_mapping(
                    user,
                    record["Risk Level"]
                )
            )

            sar_json = export_sar_as_json(sar_payload)

            st.download_button(
                label="⬇️ Download SAR (JSON)",
                data=sar_json,
                file_name=f"SAR_{case['case_id']}.json",
                mime="application/json"
            )


 
        
# =====================================================
# 🧾 GLOBAL CASE DASHBOARD
# =====================================================
elif st.session_state.mode == "🧾 Case Dashboard":

    st.markdown("## 🧾 Global AML Case Dashboard")
    st.caption("Centralized case management and audit overview")

    cases = get_cases()

    if not cases:
        st.info("No AML cases created yet.")
    else:
        # Convert cases to DataFrame
        case_rows = []
        for case in cases.values():
            case_rows.append({
                "Case ID": case["case_id"],
                "User": case["user"],
                "Status": case["status"],
                "Risk Level": case["risk_level"],
                "Created At": case["created_at"]
            })

        df_cases = pd.DataFrame(case_rows)

        # ---- Summary Metrics ----
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Cases", len(df_cases))
        c2.metric("🟡 Open", (df_cases["Status"] == "🟡 Open").sum())
        c3.metric("🕵️ Under Review", (df_cases["Status"] == "🕵️ Under Review").sum())
        c4.metric("🚨 Escalated", (df_cases["Status"] == "🚨 Escalated").sum())

        st.markdown("---")

        # ---- Case Table ----
        st.markdown("### 📋 Case Overview")
        st.dataframe(df_cases, use_container_width=True)

        st.markdown("---")

        # ---- Case Drilldown ----
        st.markdown("### 🔍 Case Drilldown")

        selected_case_id = st.selectbox(
            "Select Case ID",
            df_cases["Case ID"].tolist()
        )

        selected_case = cases[selected_case_id]

        st.write(f"**User:** `{selected_case['user']}`")
        st.write(f"**Current Status:** {selected_case['status']}")
        st.write(f"**Risk Level:** {selected_case['risk_level']}")
        st.write(f"**Created At:** {selected_case['created_at']}")

        st.markdown("#### 🧾 Audit Trail")

        audit = get_audit_trail(selected_case_id)

        if audit:
            for a in audit:
                st.write(f"[{a['time']}] {a['message']}")
        else:
            st.info("No audit activity recorded for this case.")


# =====================================================
# 🧪 MODE 3 — SIMULATION
# =====================================================
elif st.session_state.mode == "🧪 Simulation":

    st.markdown("## 🧪 Fraud Scenario Simulation")

    c1, c2, c3 = st.columns(3)

    if c1.button("💸 Simulate Smurfing"):
        target = random.choice(df["User"].tolist())
        st.session_state.dynamic_risk[target] += 0.15
        log_alert(f"💸 Smurfing injected on {target}")
        st.warning(f"Smurfing simulated on {target}")

    if c2.button("🧍‍♂️ Simulate Mule Network"):
        targets = random.sample(df["User"].tolist(), 3)
        for t in targets:
            st.session_state.dynamic_risk[t] += 0.2
        log_alert("🧍‍♂️ Mule network injected")
        st.warning(f"Mule network simulated on {', '.join(targets)}")

    if c3.button("🔁 Simulate Layering"):
        target = random.choice(df["User"].tolist())
        st.session_state.dynamic_risk[target] += 0.25
        log_alert(f"🔁 Layering injected on {target}")
        st.warning(f"Layering simulated on {target}")
