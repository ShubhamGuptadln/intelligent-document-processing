import pytesseract
from PIL import Image

def extract_image_text(path):
    text = pytesseract.image_to_string(Image.open(path))
    return text, {"ocr": True}
