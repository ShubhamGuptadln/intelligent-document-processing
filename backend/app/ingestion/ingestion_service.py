# import uuid
# import shutil
# import os
# from app.ingestion.file_validator import validate_file
# from app.ingestion.file_detector import detect_type
# from app.extraction.extraction_router import extract_text
# from app.vision.vision_gating import decide_vision
# from app.persistence.document_repository import save_document
# from app.config import STORAGE_DOCS, STORAGE_EXTRACTED

# def ingest(file):
#     doc_uuid = str(uuid.uuid4())
#     path = os.path.join(STORAGE_DOCS, f"{doc_uuid}_{file.filename}")

#     with open(path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     valid, reason = validate_file(path)
#     if not valid:
#         save_document(doc_uuid, file.filename, None, False, "manual_review", reason)
#         return {"uuid": doc_uuid, "status": "manual_review", "reason": reason}

#     file_type = detect_type(path)
#     text, stats = extract_text(path, file_type)

#     txt_path = os.path.join(STORAGE_EXTRACTED, f"{doc_uuid}.txt")
#     with open(txt_path, "w", encoding="utf-8") as f:
#         f.write(text)

#     vision_required = decide_vision(stats)

#     save_document(
#         doc_uuid, file.filename, file_type,
#         vision_required, "ingested", None
#     )

#     return {
#         "uuid": doc_uuid,
#         "file_type": file_type,
#         "vision_required": vision_required
#     }
# import uuid
# import shutil

# from app.config import STORAGE_DOCS, STORAGE_EXTRACTED
# from app.ingestion.file_validator import validate_file
# from app.ingestion.file_detector import detect_type
# from app.extraction.extraction_router import extract_text
# from app.vision.vision_gating import decide_vision

# from app.persistence.document_repository import (
#     save_document,
#     get_document_by_hash,
#     get_result_by_uuid,
#     save_document_result,
#     update_document_result_llm
# )

# from app.processing.document_classifier import classify_document
# from app.processing.routing_service import route_document
# from app.llm.gemini_client import resolve_missing_entities
# from app.utils.hash_utils import compute_file_hash


# def ingest(file):
#     doc_uuid = str(uuid.uuid4())
#     path = f"{STORAGE_DOCS}/{doc_uuid}_{file.filename}"

#     with open(path, "wb") as f:
#         shutil.copyfileobj(file.file, f)

#     file_hash = compute_file_hash(path)

#     # ---------------- DUPLICATE CHECK ----------------
#     existing_doc = get_document_by_hash(file_hash)
#     if existing_doc:
#         result = get_result_by_uuid(existing_doc.doc_uuid)
#         return {
#             "duplicate": True,
#             "uuid": existing_doc.doc_uuid,
#             "processing_result": result.__dict__ if result else None,
#             "message": "Duplicate document. Existing result returned."
#         }

#     # ---------------- PHASE 1 ----------------
#     file_type = detect_type(path) or "unknown"

#     valid, reason = validate_file(path)
#     if not valid:
#         save_document(doc_uuid, file_hash, file.filename, file_type, False, "manual_review", reason)
#         return {"uuid": doc_uuid, "status": "manual_review"}

#     text, stats = extract_text(path, file_type)

#     with open(f"{STORAGE_EXTRACTED}/{doc_uuid}.txt", "w", encoding="utf-8") as f:
#         f.write(text)

#     vision_required = decide_vision(stats)

#     save_document(doc_uuid, file_hash, file.filename, file_type, vision_required, "ingested", None)

#     # ---------------- PHASE 2 : RULE BASED ----------------
#     classification = classify_document(text)

#     team_assigned = route_document(
#         classification["doc_type"],
#         classification["all_fields_present"]
#     )

#     if classification["all_fields_present"]:
#         save_document_result(
#             doc_uuid,
#             classification["doc_type"],
#             team_assigned,
#             "rule_based",
#             classification["entities"],
#             [],
#             100.00,
#             "auto"
#         )

#         return {
#             "uuid": doc_uuid,
#             "processing_stage": "rule_based",
#             "assigned_team": team_assigned,
#             "entities": classification["entities"]
#         }

#     # ---------------- PHASE 3 : LLM ----------------
#     llm_result = resolve_missing_entities(
#         classification["doc_type"],
#         classification["entities"],
#         classification["missing_fields"],
#         text
#     )

#     merged_entities = {
#         **classification["entities"],
#         **llm_result["filled_entities"]
#     }

#     confidence = llm_result["confidence_score"]

#     if confidence >= 85:
#         decision = "auto"
#         team_assigned = route_document(classification["doc_type"], True)
#     elif confidence >= 70:
#         decision = "human_in_loop"
#         team_assigned = "Human Review"
#     else:
#         decision = "manual_review"
#         team_assigned = "Manual Review"

#     update_document_result_llm(
#         doc_uuid,
#         merged_entities,
#         confidence,
#         decision
#     )

#     return {
#         "uuid": doc_uuid,
#         "processing_stage": "llm",
#         "confidence_score": confidence,
#         "automation_decision": decision,
#         "assigned_team": team_assigned,
#         "entities": merged_entities
#     }
import uuid
import shutil

from app.config import STORAGE_DOCS, STORAGE_EXTRACTED
from app.ingestion.file_validator import validate_file
from app.ingestion.file_detector import detect_type
from app.extraction.extraction_router import extract_text
from app.vision.vision_gating import decide_vision

from app.persistence.document_repository import (
    save_document,
    get_document_by_hash,
    get_result_by_uuid,
    save_document_result,
    update_document_result_llm
)

from app.processing.document_classifier import classify_document
from app.processing.routing_service import route_document
from app.llm.gemini_client import llm_classify_and_route
from app.utils.hash_utils import compute_file_hash


def ingest(file):
    doc_uuid = str(uuid.uuid4())
    path = f"{STORAGE_DOCS}/{doc_uuid}_{file.filename}"

    # ---------------- SAVE FILE ----------------
    with open(path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    file_hash = compute_file_hash(path)

    # ---------------- DUPLICATE CHECK ----------------
    existing = get_document_by_hash(file_hash)
    if existing:
        result = get_result_by_uuid(existing.doc_uuid)
        return {
            "duplicate": True,
            "uuid": existing.doc_uuid,
            "processing_result": result.__dict__ if result else None,
            "message": "Duplicate document"
        }

    # ---------------- PHASE 1 : BASIC INGESTION ----------------
    file_type = detect_type(path) or "unknown"

    valid, reason = validate_file(path)
    if not valid:
        save_document(doc_uuid, file_hash, file.filename, file_type, False, "manual_review", reason)
        return {"uuid": doc_uuid, "status": "manual_review"}

    text, stats = extract_text(path, file_type)

    with open(f"{STORAGE_EXTRACTED}/{doc_uuid}.txt", "w", encoding="utf-8") as f:
        f.write(text)

    vision_required = decide_vision(stats)

    save_document(doc_uuid, file_hash, file.filename, file_type, vision_required, "ingested", None)

    # ---------------- PHASE 2 : RULE-BASED ----------------
    classification = classify_document(text)

    if classification["all_fields_present"]:
        team = route_document(classification["doc_type"], True)

        save_document_result(
            doc_uuid=doc_uuid,
            doc_category=classification["doc_type"],
            assigned_team=team,
            processing_stage="rule_based",
            entities=classification["entities"],
            missing_fields=[],
            confidence_score=100.0,
            automation_decision="auto"
        )

        return {
            "uuid": doc_uuid,
            "processing_stage": "rule_based",
            "assigned_team": team,
            "processing_result": {
                "doc_category": classification["doc_type"],
                "assigned_team": team,
                "processing_stage": "rule_based",
                "confidence_score": 100,
                "automation_decision": "auto",
                "entities": classification["entities"]
            }
        }

    # ---------------- PHASE 3 : LLM FALLBACK ----------------
    llm_result = llm_classify_and_route(text)

    confidence = llm_result["confidence_score"]

    if confidence >= 85:
        decision = "auto"
    elif confidence >= 70:
        decision = "human_in_loop"
    else:
        decision = "manual_review"

    update_document_result_llm(
        doc_uuid=doc_uuid,
        entities=llm_result["entities"],
        confidence_score=confidence,
        automation_decision=decision
    )

    return {
        "duplicate": False,
        "uuid": doc_uuid,
        "file_type": file_type,
        "vision_required": vision_required,
        "processing_result": {
            "doc_category": llm_result["doc_category"],
            "assigned_team": llm_result["assigned_team"],
            "processing_stage": "llm",
            "confidence_score": confidence,
            "automation_decision": decision,
            "entities": llm_result["entities"]
        }
    }
