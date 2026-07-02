import os

import streamlit as st
from dotenv import load_dotenv
from google import genai

from modules.database import PharmaDatabase
from modules.styles import load_css
from modules.medicine_card import show_medicine_card
from modules.smart_search import (
    search_anything,
    get_brand_list
)

# =====================================================
# Load Environment
# =====================================================

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

db = PharmaDatabase()

# =====================================================
# Page Config
# =====================================================

st.set_page_config(
    page_title="💊 Pharma AI",
    page_icon="💊",
    layout="wide"
)

load_css()

st.title("💊 Pharma AI")
st.caption("AI Clinical Pharmacy Assistant")

# =====================================================
# Chat History
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# =====================================================
# Chat Input
# =====================================================

question = st.chat_input(
    "દવા વિશે પ્રશ્ન પૂછો..."
)

# =====================================================
# Database Search
# =====================================================

medicine = search_anything(question)

brands = get_brand_list(medicine)

selected_brand = None

if medicine:

    st.subheader("💊 Medicine Information")

    # ------------------------------------
    # Multiple Brand Selection
    # ------------------------------------

    if brands is not None and len(brands) > 1:

        brand_options = brands["Brand_Name"].tolist()

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
    # =====================================================
# Database Search
# =====================================================

medicine = search_anything(question)

brands = get_brand_list(medicine)

selected_brand = None

if medicine:

    st.subheader("💊 Medicine Information")

    # ------------------------------------
    # Multiple Brand Selection
    # ------------------------------------

    if brands is not None and len(brands) > 1:

        brand_options = brands["Brand_Name"].tolist()

        selected_brand = st.selectbox(
            "💊 Select Brand",
            brand_options
        )

        medicine = db.get_complete_medicine(
            selected_brand
        )

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