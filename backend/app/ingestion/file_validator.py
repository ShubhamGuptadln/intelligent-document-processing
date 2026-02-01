import fitz  # PyMuPDF
from app.logger import logger

def validate_file(path: str):
    try:
        if path.lower().endswith(".pdf"):
            doc = fitz.open(path)
            if doc.is_encrypted:
                return False, "password_protected"
        return True, None
    except Exception as e:
        logger.error(f"File corrupt: {e}")
        return False, "corrupt_file"
