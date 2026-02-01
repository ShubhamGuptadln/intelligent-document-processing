# app/processing/document_classifier.py

from .entity_extractor import extract_entities, check_mandatory_fields

def classify_document(text: str):
    """
    Classify document type based on presence of keywords/entities.
    Returns (doc_type, entities_dict, all_fields_present, missing_fields)
    """
    # Simple keyword-based classification
    text_lower = text.lower()
    if "invoice" in text_lower or "total amount" in text_lower:
        doc_type = "invoice"
    elif "warranty" in text_lower or "claim" in text_lower:
        doc_type = "warranty"
    elif "feedback" in text_lower or "experience" in text_lower:
        doc_type = "feedback"
    elif "support ticket" in text_lower or "issue" in text_lower:
        doc_type = "support_ticket"
    else:
        doc_type = "unknown"

    # Extract entities
    entities = extract_entities(text)
    all_fields_present, missing_fields = check_mandatory_fields(entities, doc_type)

    return {
        "doc_type": doc_type,
        "entities": entities,
        "all_fields_present": all_fields_present,
        "missing_fields": missing_fields
    }
