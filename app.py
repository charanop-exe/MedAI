# streamlit_app.py

import streamlit as st
import PyPDF2
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

try:
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("Missing API key")

    client = Groq(api_key=api_key)

except Exception:
    st.error("🛑 Failed to initialize AI service. Check your API key.")
    st.stop()


# ---------------------------
# 2. SAFE LLAMA CALL
# ---------------------------

def get_llama_response(prompt: str) -> str:
    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": "You are a safe, professional medical AI assistant."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.5,
            max_tokens=1024
        )
        return response.choices[0].message.content

    except Exception:
        st.error("⚠️ The AI service could not process your request at the moment.")
        return ""


st.set_page_config(
    page_title="AI Medical Report Analyzer",
    page_icon="🩺",
    layout="centered"
)

st.title("🩺 AI Medical Report Analyzer")
st.write(
    "This tool provides **educational explanations** of medical reports. "
    "It does **not** diagnose or replace a healthcare professional."
)

user_query = st.text_area(
    "Your question (optional but recommended):",
    height=100,
    placeholder="Example: Explain these blood test values in simple terms."
)

uploaded_file = st.file_uploader(
    "Upload a medical report (optional):",
    type=["pdf", "png", "jpg", "jpeg"]
)

if st.button("Analyze", type="primary"):

    if not user_query and not uploaded_file:
        st.warning("Please enter a question or upload a report.")
        st.stop()

    with st.spinner("🤖 Analyzing safely..."):

        system_prompt = """
You are a medical information assistant AI.

IMPORTANT RULES (STRICT):
1. You MUST NOT diagnose diseases.
2. You MUST NOT predict conditions.
3. You MUST NOT prescribe treatments or medications.
4. You MUST NOT give direct medical instructions.
5. You MAY explain medical terms, lab values, and general concepts in simple language.
6. You MAY mention widely known educational topics ONLY as information to discuss with a doctor.
7. You MUST encourage consulting a qualified healthcare professional.
8. Your tone must be neutral, calm, and educational.
9. You MUST include the disclaimer at the end.

Your task:
• Explain the provided medical information in plain language.
• Highlight what the numbers or terms generally represent.
• Suggest 5 questions the patient can ask their doctor.

MANDATORY DISCLAIMER (must be included verbatim at the end):
---
Disclaimer: This information is for educational purposes only and is not a substitute for professional medical advice. Always consult a qualified healthcare professional regarding your health.
"""

        file_text = ""



        if uploaded_file:
            try:
                if uploaded_file.type == "application/pdf":
                    reader = PyPDF2.PdfReader(uploaded_file)
                    for page in reader.pages:
                        file_text += page.extract_text() or ""

                elif "image" in uploaded_file.type:
                    file_text = "Image uploaded. Please describe the medical findings manually."

            except Exception:
                st.error("⚠️ Failed to read uploaded file.")
                st.stop()



        full_prompt = f"""
{system_prompt}

User question:
{user_query if user_query else "No specific question provided."}

Medical report content:
{file_text if file_text else "No report uploaded."}
"""

        response = get_llama_response(full_prompt)

        if response:
            st.subheader("AI Explanation")
            st.markdown(response)


st.caption(
    "⚠️ This app provides educational explanations only. "
    "Always consult a healthcare professional for medical decisions."
)