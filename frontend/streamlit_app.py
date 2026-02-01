import os
import json
import streamlit as st
import requests
import google.generativeai as genai

# ---------------- LLM CONFIG ----------------
# Make sure you have your API key in environment variable
genai.configure(api_key="AIzaSyA2pBQBIW-50TpsRlpsxHvurazmH6HNiS8")
MODEL_NAME = "gemini-3-flash-preview"

# ---------------- LLM HELPER ----------------
def resolve_missing_entities(doc_type, extracted_entities, missing_fields, text_snippet):
    """
    Uses LLM to fill missing fields only.
    Returns dict: {"filled_entities": {...}, "confidence_score": ...}
    """
    if not missing_fields:
        return {"filled_entities": {}, "confidence_score": 100}

    prompt = f"""
You are an enterprise document processing AI.

Document Type: {doc_type}

Already extracted entities (JSON):
{json.dumps(extracted_entities, indent=2)}

Missing fields:
{missing_fields}

Text snippet (partial, noisy):
{text_snippet[:3000]}

Rules:
- ONLY fill missing fields
- Return strict JSON
- Add confidence score (0-100)
- Mention source sentence if possible

Return format:
{{
  "filled_entities": {{ }},
  "confidence_score": number
}}
"""
    try:
        model = genai.GenerativeModel(MODEL_NAME)
        response = model.generate_content(prompt)
        return json.loads(response.text)
    except Exception:
        return {"filled_entities": {}, "confidence_score": 0}

# ---------------- STREAMLIT APP ----------------
st.set_page_config(page_title="IDAP – Final Output", layout="centered")
st.title("📄 Intelligent Document Processing Agent")

file = st.file_uploader(
    "Upload document (PDF / DOCX / Image)",
    type=["pdf", "docx", "png", "jpg", "jpeg"]
)

if file:
    with st.spinner("Processing document..."):
        try:
            res = requests.post(
                "http://localhost:8000/upload",
                files={"file": file}
            )
        except Exception as e:
            st.error("❌ Failed to call API")
            st.text(str(e))
            st.stop()

    if res.status_code == 200:
        data = res.json()
        st.success("✅ Processing completed")

        st.subheader("📌 Final Output")
        st.json(data)

        # ---------------- Safe handling of processing_result ----------------
        pr = data.get("processing_result") or {}
        doc_type = pr.get("doc_category", "unknown")
        assigned_team = pr.get("assigned_team", "Human in Loop")
        processing_stage = pr.get("processing_stage", "N/A")
        automation_decision = pr.get("automation_decision", "human_in_loop")
        confidence_score = pr.get("confidence_score", "N/A")
        entities = pr.get("entities", {})

        # ---------------- LLM ENTITY FILLING ----------------
        missing_fields = pr.get("missing_fields", [])
        if missing_fields:
            filled = resolve_missing_entities(doc_type, entities, missing_fields, data.get("text", ""))
            entities.update(filled.get("filled_entities", {}))
            confidence_score = filled.get("confidence_score", confidence_score)

        # ---------------- Display Summary ----------------
        st.markdown("### 🧠 Decision Summary")
        st.markdown(f"""
        - **Document Type**: `{doc_type}`
        - **Assigned Team**: `{assigned_team}`
        - **Processing Stage**: `{processing_stage}`
        - **Confidence Score**: `{confidence_score}`
        - **Automation Decision**: `{automation_decision}`
        """)

        st.markdown("### 📊 Extracted / Final Entities")
        st.json(entities)

    else:
        st.error("❌ Processing failed")
        st.text(res.text)
