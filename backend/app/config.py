import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))

STORAGE_DOCS = os.path.join(BASE_DIR, "storage/documents")
STORAGE_EXTRACTED = os.path.join(BASE_DIR, "storage/extracted/raw")

os.makedirs(STORAGE_DOCS, exist_ok=True)
os.makedirs(STORAGE_EXTRACTED, exist_ok=True)

MYSQL_URL = "mysql+pymysql://root:Shubh%406387@localhost:3306/idap"
