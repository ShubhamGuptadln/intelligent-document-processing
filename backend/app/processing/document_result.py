# app/models/document_result.py
from sqlalchemy import Column, String, BigInteger, DECIMAL, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.mysql import JSON
from sqlalchemy.sql import func
from app.base import Base

class DocumentResult(Base):
    __tablename__ = "document_results"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    doc_uuid = Column(String(64), ForeignKey("documents.doc_uuid"))

    doc_category = Column(String(50))
    assigned_team = Column(String(50))
    processing_stage = Column(String(30))

    entities = Column(JSON)
    missing_fields = Column(JSON)

    confidence_score = Column(DECIMAL(5, 2))
    automation_decision = Column(String(30))

    created_at = Column(TIMESTAMP, server_default=func.now())
