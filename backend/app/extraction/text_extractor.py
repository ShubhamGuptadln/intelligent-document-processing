import fitz
from docx import Document

def extract_text_doc(path):
    doc = Document(path)
    return "\n".join([p.text for p in doc.paragraphs])

def extract_text_pdf(path):
    doc = fitz.open(path)
    text = ""
    image_pages = 0
    for page in doc:
        text += page.get_text()
        if page.get_images():
            image_pages += 1
    return text, {"pages": len(doc), "image_pages": image_pages}
