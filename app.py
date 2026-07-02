import streamlit as st
import os
from dotenv import load_dotenv
from google import genai

from modules.styles import load_css
from modules.smart_search import search_anything
from modules.medicine_card import show_medicine_card

# ---------------------------------------
# Load Environment
# ---------------------------------------

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

# ---------------------------------------
# Page Config
# ---------------------------------------

st.set_page_config(
    page_title="Pharma AI",
    page_icon="💊",
    layout="wide"
)

load_css()

st.title("💊 Pharma AI")
st.caption("AI Clinical Pharmacy Assistant")

# ---------------------------------------
# Chat History
# ---------------------------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# ---------------------------------------
# Chat Input
# ---------------------------------------

question = st.chat_input(
    "દવા વિશે પ્રશ્ન પૂછો..."
)

if question:

    st.session_state.messages.append(
        {
            "role": "user",
            "content": question
        }
    )

    with st.chat_message("user"):
        st.markdown(question)

    # ---------------------------------------
    # Database Search
    # ---------------------------------------

    medicine = search_anything(question)

    if medicine:

        st.subheader("💊 Medicine Information")

        show_medicine_card(medicine)

        st.divider()

        st.subheader("🤖 AI Clinical Pharmacist")

        medicine_database = f"""
Brand Name: {medicine['brand']['Brand_Name']}
Generic Name: {medicine['generic']['Generic_Name']}
Gujarati Name: {medicine['generic']['Generic_Name_Gujarati']}
Strength: {medicine['brand']['Strength']}
Dosage Form: {medicine['brand']['Dosage_Form']}
Company: {medicine['company']['Company_Name']}
Country: {medicine['company']['Country']}
Pack Size: {medicine['product']['Pack_Size']}
Schedule: {medicine['product']['Schedule']}
GST: {medicine['product']['GST']}
"""

    else:

        st.warning(
            "⚠️ Medicine not found in database.\n\nAI will answer using general educational information."
        )

        medicine_database = "Medicine not found in database."
            # ---------------------------------------
    # Gemini AI
    # ---------------------------------------

    prompt = f"""
You are an experienced Clinical Pharmacist.

Respond ONLY in Gujarati.

The response must always follow this format.

💊 દવાનું નામ

🧬 Generic Name

✅ ઉપયોગ

⚙️ દવા કેવી રીતે કાર્ય કરે છે?

💊 સામાન્ય માત્રા
(General educational information only)

⚠️ સામાન્ય આડઅસરો

🚫 ક્યારે સાવચેતી રાખવી?

🤰 ગર્ભાવસ્થા

🤱 સ્તનપાન

🧑‍⚕️ દર્દી માટે સલાહ

📚 મહત્વપૂર્ણ નોંધ

Rules:

• Use simple Gujarati.
• Use bullet points.
• Never diagnose diseases.
• Never prescribe medicines.
• Never recommend a dose for a specific patient.
• If information is unavailable, write:
"માહિતી ઉપલબ્ધ નથી."

Medicine Database

{medicine_database}

User Question

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        answer = response.text

    except Exception:

        answer = """
### ⚠️ AI સેવા હાલમાં ઉપલબ્ધ નથી

સંભવિત કારણો:

• Gemini API quota પૂર્ણ થઈ ગઈ છે.
• Internet Connection ઉપલબ્ધ નથી.
• Gemini Server વ્યસ્ત છે.

✅ Database માહિતી સફળતાપૂર્વક ઉપલબ્ધ છે.
"""

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": answer
        }
    )

    with st.chat_message("assistant"):
        st.markdown(answer)