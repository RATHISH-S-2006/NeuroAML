"""
AML Case Management & Audit Trail
Handles lifecycle of suspicious accounts
"""

import streamlit as st
from datetime import datetime
import uuid


# -----------------------------------------------------
# Case Store Initialization
# -----------------------------------------------------
def initialize_case_store():
    if "cases" not in st.session_state:
        st.session_state.cases = {}

    if "audit_trail" not in st.session_state:
        st.session_state.audit_trail = []


# -----------------------------------------------------
# Case Creation
# -----------------------------------------------------
def create_case(user, risk_level):
    initialize_case_store()

    # Prevent duplicate cases
    for case in st.session_state.cases.values():
        if case["user"] == user and case["status"] != "Closed":
            return case

    case_id = f"CASE-{uuid.uuid4().hex[:8].upper()}"

    case = {
        "case_id": case_id,
        "user": user,
        "status": "🟡 Open",
        "risk_level": risk_level,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "actions": []
    }

    st.session_state.cases[case_id] = case
    log_audit(case_id, f"Case created for {user} with risk level {risk_level}")

    return case


# -----------------------------------------------------
# Case Update Actions
# -----------------------------------------------------
def update_case_status(case_id, new_status, note=""):
    initialize_case_store()

    case = st.session_state.cases.get(case_id)
    if not case:
        return

    case["status"] = new_status
    case["actions"].append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "action": new_status,
        "note": note
    })

    log_audit(case_id, f"Status changed to {new_status}. {note}")


# -----------------------------------------------------
# Audit Trail Logger
# -----------------------------------------------------
def log_audit(case_id, message):
    st.session_state.audit_trail.append({
        "time": datetime.now().strftime("%H:%M:%S"),
        "case_id": case_id,
        "message": message
    })


# -----------------------------------------------------
# Retrieve Cases
# -----------------------------------------------------
def get_cases():
    initialize_case_store()
    return st.session_state.cases


def get_audit_trail(case_id=None):
    initialize_case_store()

    if case_id:
        return [
            a for a in st.session_state.audit_trail
            if a["case_id"] == case_id
        ]
    return st.session_state.audit_trail
