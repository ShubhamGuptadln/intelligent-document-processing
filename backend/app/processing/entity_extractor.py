# app/processing/entity_extractor.py

import re
from .rules import ENTITY_RULES, MANDATORY_FIELDS

def extract_entities(text: str):
    """
    Extract all possible entities based on regex rules.
    Returns a dict of entity_name -> list of found values.
    """
    extracted = {}
    for entity, pattern in ENTITY_RULES.items():
        matches = re.findall(pattern, text)
        extracted[entity] = matches if matches else []
    return extracted


def check_mandatory_fields(extracted_entities: dict, doc_type: str):
    """
    Check if all mandatory fields for this document type exist.
    Returns (bool: all_fields_present, list: missing_fields)
    """
    missing = []
    for field in MANDATORY_FIELDS.get(doc_type, []):
        if not extracted_entities.get(field):
            missing.append(field)
    return (len(missing) == 0, missing)
