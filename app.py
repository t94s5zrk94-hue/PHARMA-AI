import logging
import streamlit as st
from typing import Any, Optional, Final, TypeAlias
from dotenv import load_dotenv

# Type Alias for better readability
MedicineData: TypeAlias = dict[str, Any]

# Environment initialization
load_dotenv()

# Logging configuration
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger: Final = logging.getLogger(__name__)

from pharma_ai.ai.engine import ask_ai
from pharma_ai.services.database import PharmaDatabase
from pharma_ai.services.smart_search import search_anything, get_brand_list
from pharma_ai.ui.medicine_card import show_medicine_card
from pharma_ai.ui.interaction import DrugInteraction
from pharma_ai.ui.styles import load_css

# Constants
MSG_USER: Final = "user"
MSG_ASSISTANT: Final = "assistant"
KEY_MESSAGES: Final = "messages"
KEY_RESULT: Final = "search_result"

@st.cache_resource
def get_database() -> PharmaDatabase:
    try:
        return PharmaDatabase()
    except Exception as e:
        logger.error(f"Database initialization failed: {e}")
        st.error("Critical System Error: Database unavailable.")
        st.stop()

def configure_app() -> None:
    st.set_page_config(page_title="Pharma AI", page_icon="💊", layout="wide")
    load_css()

def initialize_session() -> None:
    if KEY_MESSAGES not in st.session_state:
        st.session_state[KEY_MESSAGES] = []
    if KEY_RESULT not in st.session_state:
        st.session_state[KEY_RESULT] = None

def build_ai_context(medicine: MedicineData) -> str:
    b = medicine.get("brand", {})
    g = medicine.get("generic", {})
    c = medicine.get("company", {})
    p = medicine.get("product", {})
    
    fields = [
        ("Brand Name", b.get("Brand_Name")),
        ("Generic Name", g.get("Generic_Name")),
        ("Strength", b.get("Strength")),
        ("Dosage Form", b.get("Dosage_Form")),
        ("Company", c.get("Company_Name")),
        ("Schedule", p.get("Schedule")),
        ("Pack Size", p.get("Pack_Size")),
        ("Ingredients", g.get("Ingredients"))
    ]
    return "\n".join(f"{label}: {value or 'N/A'}" for label, value in fields)

def process_question(question: str) -> None:

    # Every new search starts a fresh conversation
    st.session_state[KEY_MESSAGES] = []

    result = search_anything(question)
    st.session_state[KEY_RESULT] = result

    st.session_state[KEY_MESSAGES].append(
        {"role": MSG_USER, "content": question}
    )
    
    if result and "data" in result:
        medicine: MedicineData = result["data"]
        # Contract validation
        if all(k in medicine for k in ["brand", "generic", "company", "product"]):
            context = build_ai_context(medicine)
            with st.spinner("Clinical pharmacist is preparing response..."):
                response = ask_ai(question, context)
            st.session_state[KEY_MESSAGES].append({ "role": MSG_ASSISTANT, "content": response })
        else:
            logger.error("Database contract violation: Missing keys in medicine object.")
            st.error("Unexpected data format received. Please contact support.")
    else:
        st.session_state[KEY_MESSAGES].append({ "role": MSG_ASSISTANT, "content": "Medicine not found." })
    st.rerun()

def main() -> None:
    configure_app()
    initialize_session()
    db = get_database()
    
    st.title("💊 Pharma AI")
    
    with st.sidebar:
        st.subheader("💊 Drug Interaction Checker")
        m1 = st.text_input("Medicine 1")
        m2 = st.text_input("Medicine 2")
        if st.button("Check Interaction"):
            res = DrugInteraction().check_interaction(m1, m2)

            st.write(res.get("interaction", "Error")) 

    result = st.session_state[KEY_RESULT]
    
    if result and "data" in result:

        medicine: MedicineData = result["data"]

        # Pass display name to UI
        medicine["display_name"] = result.get("display_name")

        #st.write(medicine.keys()) # temporary debug

        show_medicine_card(medicine)
        
        brands = get_brand_list(result)
        if not brands.empty:
            options = brands["Brand_Name"].unique().tolist()
            selected = st.selectbox("Select Brand", options, index=0)
            
            if selected != medicine.get("brand", {}).get("Brand_Name"):
                new_data = db.get_complete_medicine(selected)
                if new_data:
                    st.session_state[KEY_RESULT]["data"] = new_data
                    st.rerun()

    st.subheader("🤖 Clinical Assistant")
    for msg in st.session_state[KEY_MESSAGES]:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])
            
    if prompt := st.chat_input("Ask a question..."):
        process_question(prompt)

if __name__ == "__main__":
    main()