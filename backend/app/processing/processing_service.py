# app/processing/processing_service.py

from app.processing.document_classifier import classify_document
from app.processing.routing_service import route_document
from app.persistence.document_repository import save_document_result

def process_document(doc_uuid: str, text: str, vision_required: bool):
    classification_result = classify_document(text)

    team_assigned = route_document(
        classification_result["doc_type"],
        classification_result["all_fields_present"]
    )

    save_document_result(
        doc_uuid=doc_uuid,
        doc_category=classification_result["doc_type"],
        assigned_team=team_assigned,
        processing_stage="rule_based",
        entities=classification_result["entities"],
        missing_fields=classification_result["missing_fields"],
        confidence_score=None,
        automation_decision="pending"
    )

    return {
        "doc_category": classification_result["doc_type"],
        "assigned_team": team_assigned,
        "entities": classification_result["entities"],
        "missing_fields": classification_result["missing_fields"]
    }
