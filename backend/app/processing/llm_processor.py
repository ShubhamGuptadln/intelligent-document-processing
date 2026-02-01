from app.llm.gemini_client import fill_missing_fields

def llm_enrichment(doc_type, entities, missing_fields):
    llm_result = fill_missing_fields(
        doc_type=doc_type,
        extracted_entities=entities,
        missing_fields=missing_fields
    )

    confidence = llm_result["confidence_score"]

    if confidence >= 85:
        decision = "auto"
    elif confidence >= 70:
        decision = "human_in_loop"
    else:
        decision = "manual_review"

    return {
        "filled_fields": llm_result["filled_fields"],
        "confidence_score": confidence,
        "automation_decision": decision,
        "explanation": llm_result.get("explanation", {})
    }
