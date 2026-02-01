# app/processing/routing_service.py

# Mapping document type to team
TEAM_MAPPING = {
    "invoice": "Finance Team",
    "warranty": "Warranty Team",
    "feedback": "Customer Feedback Team",
    "support_ticket": "Support Team",
    "unknown": "Manual Review Team"
}

def route_document(doc_type: str, all_fields_present: bool):
    """
    Decide team assignment based on doc type and field completeness.
    """
    if not all_fields_present:
        return "Human in Loop"  # Missing fields
    return TEAM_MAPPING.get(doc_type, "Manual Review Team")
