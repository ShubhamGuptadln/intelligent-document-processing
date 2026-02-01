import re

# Regex patterns for different entity types
ENTITY_RULES = {
    "date": r"\b\d{2}[-/]\d{2}[-/]\d{4}\b",
    "amount": r"(?:₹|\$)\s?\d+(?:,\d{3})*(?:\.\d+)?",
    "customer_id": r"CUST[-_]?\d{3,10}",
    "email": r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    "name": r"Name\s*:\s*([A-Za-z ]+)",
}

# Mandatory fields by document type
MANDATORY_FIELDS = {
    "invoice": ["date", "amount", "customer_id"],
    "warranty": ["date", "customer_id", "name"],
    "feedback": ["date", "email", "name"],
    "support_ticket": ["date", "customer_id", "email"]
}