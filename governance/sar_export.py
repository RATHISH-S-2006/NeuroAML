"""
SAR (Suspicious Activity Report) Export Module
Generates regulator-style AML reports
"""

from datetime import datetime
import json


def generate_sar_payload(
    case,
    evidence,
    typologies,
    forecast,
    compliance_rules
):
    """
    Generates structured SAR payload (JSON-ready).
    """

    sar = {
        "report_type": "Suspicious Activity Report (SAR)",
        "generated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "case_id": case["case_id"],
        "subject_account": case["user"],
        "risk_level": case["risk_level"],
        "case_status": case["status"],
        "summary": (
            "Suspicious financial activity detected through "
            "behavioral, network, and temporal analysis."
        ),
        "evidence": evidence,
        "fraud_typologies": [
            {
                "type": t["type"],
                "justification": t["reason"]
            } for t in typologies
        ],
        "risk_forecast": forecast,
        "compliance_mapping": compliance_rules,
        "recommended_action": (
            "Immediate regulatory review and enhanced monitoring"
            if case["risk_level"] == "HIGH"
            else "Continued monitoring and due diligence"
        )
    }

    return sar


def export_sar_as_json(sar_payload):
    """
    Returns SAR report as downloadable JSON string.
    """
    return json.dumps(sar_payload, indent=4)
