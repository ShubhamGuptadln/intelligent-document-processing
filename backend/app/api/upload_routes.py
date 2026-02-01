from fastapi import APIRouter, UploadFile, File
from app.ingestion.ingestion_service import ingest

router = APIRouter()

@router.post("/upload")
def upload(file: UploadFile = File(...)):
    return ingest(file)
