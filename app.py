# streamlit_app.py
# V6: FINAL - Includes a safe, educational section on dietary topics.

import os
import streamlit as st # type: ignore
import google.generativeai as genai # type: ignore
from dotenv import load_dotenv # type: ignore

# --- 1. API and Model Configuration ---

try:
    load_dotenv()
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        st.error("🛑 Gemini API key not found. Please create a .env file and add your key.")
        st.stop()
    
    genai.configure(api_key=api_key)

except Exception as e:
    st.error(f"An error occurred during API configuration: {e}")
    st.stop()

# --- 2. The Core AI Function ---

def get_gemini_response(full_prompt: str, file_parts: list) -> str:
    """
    Uses the Gemini API to get a response based on a full prompt and optional file parts.
    """
    try:
        model = genai.GenerativeModel('gemini-2.5-flash')
        content = [full_prompt] + file_parts
        response = model.generate_content(content)
        return response.text
        
    except Exception as e:
        st.error(f"An error occurred while calling the Gemini API: {e}")
        return ""


# --- 3. The Streamlit User Interface ---

# Set the page configuration
st.set_page_config(
    page_title="AI Medical Report Analyzer",
    page_icon="🩺",
    layout="centered"
)

# Display the main title and a brief description
st.title("🩺 AI Medical Report Analyzer")
st.write("Enter your query and optionally upload a medical report for a safe, simplified analysis.")

# --- Text Input Area ---
user_query = st.text_area(
    "**Your Question or Instruction:**",
    height=100,
    placeholder="e.g., 'Summarize this report for me' or 'My blood pressure is 150/90, what does this mean?'"
)

# --- File Uploader Area (Optional) ---
uploaded_file = st.file_uploader(
    "**Upload a report for context (Optional):**",
    type=["pdf", "png", "jpg", "jpeg"]
)

# Button to trigger the analysis
if st.button("Analyze", type="primary"):
    if not user_query:
        st.warning("Please enter your question or instruction in the text box.")
        st.stop()

    with st.spinner("🤖 Analyzing safely..."):
        
        # --- THIS IS THE UPDATED, MORE ADVANCED PROMPT ---
        system_prompt = """
        **Your Role:** You are a highly skilled medical assistant AI. Your task is to analyze the user's question and any provided medical documents. You must provide a simplified, easy-to-understand response for a patient.

        **CRITICAL SAFETY RULES - YOU MUST FOLLOW THESE:**
        1.  **DO NOT DIAGNOSE:** Never state a specific diagnosis like "You have Stage 2 Hypertension." Instead, describe the numbers in a neutral way (e.g., "This reading is in the elevated range.").
        2.  **DO NOT GIVE DIRECT ADVICE:** Never tell the user what they *should* do (e.g., "You must reduce salt").
        3.  **ALWAYS DEFER TO A DOCTOR:** Your primary recommended action must always be to "discuss these results with your doctor."
        4.  **EDUCATE SAFELY (NEW RULE):** If the user's query is about a condition where diet is relevant (like blood pressure or cholesterol), you MAY include a section titled "### Dietary Topics to Discuss with Your Doctor". In this section, provide general, educational information about well-known dietary approaches (like the DASH diet) or nutrients. Frame everything as a topic for a future conversation with their doctor, not as a direct command.
        5.  **DO NOT GIVE DIRECT ADVICE:** Never tell the user what they *should* do (e.g., "You must reduce salt").
        6.  **MANDATORY DISCLAIMER:** You MUST conclude your entire response with the disclaimer: "--- \n*__Disclaimer:__ This is not a substitute for professional medical advice. Always discuss your health and any dietary changes with your doctor.*"
        7.  **STAY WITHIN YOUR ROLE:** You are an assistant providing information based on the user's input and uploaded documents. You are NOT a doctor.
        8.  **CONFIDENTIALITY:** Treat all user data as confidential.
        9.  **DO NOT REPLY TO USER:** You are not a doctor. You are an assistant. You must not reply to the user.
        10. **Give 3 questions to ask to the doctor.**

        **Guidelines:**
        Analyze the user's request below based on these rules.
        """

        # Combine the safe system prompt with the user's question
        full_prompt = f"{system_prompt}\n\n**User's Request:** '{user_query}'"

        file_parts = []
        if uploaded_file is not None:
            file_data = uploaded_file.read()
            file_parts = [
                {
                    "mime_type": uploaded_file.type,
                    "data": file_data
                }
            ]

        response = get_gemini_response(full_prompt, file_parts)

        if response:
            st.subheader("AI Analysis")
            st.markdown(response)


# python -m venv venv
# venv\Scripts\activate
# streamlit
# google-generativeai
# python-dotenv
# pip install -r requirements.txt
# streamlit run app.py