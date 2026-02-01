# from sqlalchemy import Column, String, Boolean, BigInteger, TIMESTAMP
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.sql import func

# Base = declarative_base()

# class Document(Base):
#     __tablename__ = "documents"

#     id = Column(BigInteger, primary_key=True, autoincrement=True)
#     doc_uuid = Column(String(64), unique=True, nullable=False)
#     filename = Column(String(255), nullable=False)
#     file_type = Column(String(50))
#     vision_required = Column(Boolean, default=False)
#     status = Column(String(30))
#     reason = Column(String(255))
#     created_at = Column(TIMESTAMP, server_default=func.now())


# app/models/document.py
from sqlalchemy import Column, String, Boolean, TIMESTAMP
from sqlalchemy.sql import func
from .base import Base

class Document(Base):
    __tablename__ = "documents"

    doc_uuid = Column(String(64), primary_key=True)  # make doc_uuid PK
    file_hash = Column(String(64), unique=True, index=True)
    filename = Column(String(255))
    file_type = Column(String(50))
    vision_required = Column(Boolean)
    status = Column(String(30))
    reason = Column(String(255))
    created_at = Column(TIMESTAMP, server_default=func.now())
