# from app.database import SessionLocal
# from app.models import Document

# def save_document(uuid, filename, file_type, vision, status, reason=None):
#     db = SessionLocal()
#     try:
#         doc = Document(
#             doc_uuid=uuid,
#             filename=filename,
#             file_type=file_type,
#             vision_required=vision,
#             status=status,
#             reason=reason
#         )
#         db.add(doc)
#         db.commit()
#     except Exception as e:
#         db.rollback()
#         print("DB Error:", e)
#         raise e
#     finally:
#         db.close()

from app.database import SessionLocal
from app.models import Document
from app.database import SessionLocal
from app.processing.document_result import DocumentResult


def get_document_by_hash(file_hash: str):
    db = SessionLocal()
    doc = db.query(Document).filter(Document.file_hash == file_hash).first()
    db.close()
    return doc

def get_result_by_uuid(doc_uuid: str):
    db = SessionLocal()
    result = db.query(DocumentResult)\
               .filter(DocumentResult.doc_uuid == doc_uuid)\
               .first()
    db.close()
    return result


def save_document(uuid, file_hash, filename, file_type, vision, status, reason):
    db = SessionLocal()
    doc = Document(
        doc_uuid=uuid,
        file_hash=file_hash,
        filename=filename,
        file_type=file_type,
        vision_required=vision,
        status=status,
        reason=reason
    )

    db.add(doc)
    db.commit()
    db.close()

from app.database import SessionLocal
from app.processing.document_result import DocumentResult

def save_document_result(
    doc_uuid,
    doc_category,
    assigned_team,
    processing_stage,
    entities,
    missing_fields,
    confidence_score,
    automation_decision
):
    db = SessionLocal()
    result = DocumentResult(
        doc_uuid=doc_uuid,
        doc_category=doc_category,
        assigned_team=assigned_team,
        processing_stage=processing_stage,
        entities=entities,
        missing_fields=missing_fields,
        confidence_score=confidence_score,
        automation_decision=automation_decision
    )
    db.add(result)
    db.commit()
    db.close()

def update_document_result_llm(
    doc_uuid,
    entities,
    confidence_score,
    automation_decision
):
    db = SessionLocal()
    result = db.query(DocumentResult)\
               .filter(DocumentResult.doc_uuid == doc_uuid)\
               .first()

    if result:
        result.entities = entities
        result.processing_stage = "llm"
        result.confidence_score = confidence_score
        result.automation_decision = automation_decision
        db.commit()

    db.close()

