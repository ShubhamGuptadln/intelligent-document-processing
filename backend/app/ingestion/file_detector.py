import mimetypes

def detect_type(path: str):
    mime, _ = mimetypes.guess_type(path)
    if not mime:
        return "unknown"
    if "image" in mime:
        return "image"
    if "pdf" in mime:
        return "pdf"
    if "text" in mime:
        return "text"
    if "word" in mime:
        return "doc"
    return "other"
