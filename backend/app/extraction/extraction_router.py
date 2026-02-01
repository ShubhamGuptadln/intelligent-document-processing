from app.extraction.text_extractor import extract_text_pdf, extract_text_doc
from app.extraction.ocr_extractor import extract_image_text

def extract_text(path, file_type):
    if file_type == "pdf":
        return extract_text_pdf(path)
    if file_type == "doc":
        return extract_text_doc(path), {}
    if file_type == "image":
        return extract_image_text(path)
    with open(path, "r", errors="ignore") as f:
        return f.read(), {}
