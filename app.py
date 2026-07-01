import streamlit as st
import os
from dotenv import load_dotenv
from google import genai
from modules.search import search_medicine

# Load API Key
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

st.set_page_config(
    page_title="Pharma AI",
    page_icon="💊",
    layout="wide"
)

st.title("💊 Pharma AI")
st.caption("AI Pharmacy Assistant")

# Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Chat History
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# Chat Input
question = st.chat_input("દવા વિશે પ્રશ્ન પૂછો...")

if question:

    st.session_state.messages.append(
        {"role": "user", "content": question}
    )

    with st.chat_message("user"):
        st.markdown(question)
# Search Medicine Database
result, result_type = search_medicine(question)

medicine_info = ""

if result is not None:
    medicine = result.iloc[0]

    medicine_info = f"""
Database Result

Type: {result_type}

{medicine.to_string()}
"""

    st.info(medicine_info)

    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"""
You are Pharma AI.

Rules:
- Reply only in Gujarati.
- Give educational information only.
- Never diagnose diseases.
- Never prescribe medicines.

Question:
{question}
"""
    )

    answer = response.text

    st.session_state.messages.append(
        {"role": "assistant", "content": answer}
    )

    with st.chat_message("assistant"):
        st.markdown(answer)