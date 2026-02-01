# # streamlit_app.py
# # PRODUCTION-SAFE Medical AI (Gemini + Streamlit Cloud)

# import streamlit as st
# import google.generativeai as genai

# # ---------------------------
# # 1. API CONFIGURATION
# # ---------------------------

# try:
#     api_key = st.secrets["GEMINI_API_KEY"]
#     genai.configure(api_key=api_key)
# except KeyError:
#     st.error("🛑 Gemini API key not found. Please add it in Streamlit → Settings → Secrets.")
#     st.stop()
# except Exception:
#     st.error("🛑 Failed to initialize AI service. Please try again later.")
#     st.stop()

# # ---------------------------
# # 2. SAFE GEMINI CALL
# # ---------------------------

# def get_gemini_response(prompt: str, file_parts: list) -> str:
#     try:
#         model = genai.GenerativeModel("gemini-1.5-flash")
#         response = model.generate_content([prompt] + file_parts)
#         return response.text

#     except Exception as e:
#         # Do NOT expose internal error details to users
#         st.error("⚠️ The AI service could not process your request at the moment.")
#         return ""

# # ---------------------------
# # 3. STREAMLIT UI
# # ---------------------------

# st.set_page_config(
#     page_title="AI Medical Report Analyzer",
#     page_icon="🩺",
#     layout="centered"
# )

# st.title("🩺 AI Medical Report Analyzer")
# st.write(
#     "This tool provides **educational explanations** of medical reports. "
#     "It does **not** diagnose or replace a healthcare professional."
# )

# user_query = st.text_area(
#     "Your question (optional but recommended):",
#     height=100,
#     placeholder="Example: Explain these blood test values in simple terms."
# )

# uploaded_file = st.file_uploader(
#     "Upload a medical report (optional):",
#     type=["pdf", "png", "jpg", "jpeg"]
# )

# # ---------------------------
# # 4. BUTTON ACTION
# # ---------------------------

# if st.button("Analyze", type="primary"):

#     if not user_query and not uploaded_file:
#         st.warning("Please enter a question or upload a report.")
#         st.stop()

#     with st.spinner("🤖 Analyzing safely..."):

#         # ---------------------------
#         # SAFE SYSTEM PROMPT (Gemini-Compliant)
#         # ---------------------------

#         system_prompt = """
# You are a medical information assistant AI.

# IMPORTANT RULES (STRICT):
# 1. You MUST NOT diagnose diseases.
# 2. You MUST NOT predict conditions.
# 3. You MUST NOT prescribe treatments or medications.
# 4. You MUST NOT give direct medical instructions.
# 5. You MAY explain medical terms, lab values, and general concepts in simple language.
# 6. You MAY mention widely known educational topics (e.g., DASH diet) ONLY as information to discuss with a doctor.
# 7. You MUST encourage consulting a qualified healthcare professional.
# 8. Your tone must be neutral, calm, and educational.
# 9. You MUST include the disclaimer at the end.

# Your task:
# • Explain the provided medical information in plain language.
# • Highlight what the numbers or terms generally represent.
# • Suggest 3 questions the patient can ask their doctor.

# MANDATORY DISCLAIMER (must be included verbatim at the end):
# ---
# Disclaimer: This information is for educational purposes only and is not a substitute for professional medical advice. Always consult a qualified healthcare professional regarding your health.
# """

#         full_prompt = f"""
# {system_prompt}

# User question:
# {user_query if user_query else "No specific question provided."}
# """

#         file_parts = []
#         if uploaded_file:
#             file_parts.append({
#                 "mime_type": uploaded_file.type,
#                 "data": uploaded_file.read()
#             })

#         response = get_gemini_response(full_prompt, file_parts)

#         if response:
#             st.subheader("AI Explanation")
#             st.markdown(response)

# # ---------------------------
# # 5. FOOTER
# # ---------------------------

# st.caption(
#     "⚠️ This app provides educational explanations only. "
#     "Always consult a healthcare professional for medical decisions."
# )

import streamlit as st
from google import genai

import sys
st.write(sys.version)

st.title("Gemini Smoke Test")

client = genai.Client(api_key=st.secrets["GEMINI_API_KEY"])

response = client.models.generate_content(
    model="gemini-1.5-flash",
    contents="Say hello in one sentence."
)

st.write(response.text)

