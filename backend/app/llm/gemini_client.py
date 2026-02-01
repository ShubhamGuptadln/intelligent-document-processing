import os
import json
import google.generativeai as genai

genai.configure(api_key="API_EY")

MODEL_NAME = "gemini-3-flash-preview"

def llm_classify_and_route(text: str):
    """
    LLM acts as decision-maker:
    - Document type
    - Entity inference
    - Team routing
    - Automation confidence
    """

    prompt = f"""
You are an enterprise Intelligent Document Processing AI.

Analyze the document text below and decide:

Tasks:
1. Identify document category:
   - invoice
   - warranty_claim
   - support_feedback
   - receipt
   - other

2. Extract or infer important entities if possible.
3. Decide which team should handle it:
   - Finance
   - Support
   - Warranty
   - Operations

4. Give confidence score (0–100) for automation.

Rules:
- Use reasoning even if fields are missing
- Do NOT hallucinate precise numbers if not present
- Return STRICT JSON only

Document text:
{text[:3000]}

Return JSON:
{{
  "doc_category": "",
  "assigned_team": "",
  "entities": {{}},
  "confidence_score": number
}}
"""

    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return json.loads(response.text)

    except Exception as e:
        return {
            "doc_category": "unknown",
            "assigned_team": "Manual Review",
            "entities": {},
            "confidence_score": 0
        }