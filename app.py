from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Any

import streamlit as st
from dotenv import load_dotenv

from modules.ai_engine import ask_ai
from modules.database import PharmaDatabase
from modules.medicine_card import show_medicine_card
from modules.smart_search import get_brand_list, search_anything
from modules.comparison import BrandComparison
from modules.interaction import DrugInteraction
from modules.styles import load_css



PLACEHOLDER_BRAND = re.compile(
    r"^brand\s+[a-z0-9_-]+$",
    flags=re.IGNORECASE,
)
NOT_FOUND_CONTEXT = "Medicine not found in the database."


@dataclass(frozen=True)
class SearchResult:
    """Store a medicine match and its available verified brands."""

    medicine: dict[str, Any] | None
    brand_names: tuple[str, ...] = ()


def configure_app() -> None:
    """Configure Streamlit before rendering the interface."""

    st.set_page_config(
        page_title="Pharma AI",
        page_icon="💊",
        layout="wide",
    )
    load_css()


@st.cache_resource
def get_database() -> PharmaDatabase:
    """Load and reuse the CSV-backed medicine database."""

    return PharmaDatabase()


def initialize_session() -> None:
    """Initialize application session state."""

    if "messages" not in st.session_state:
        st.session_state.messages = []

    if "search_result" not in st.session_state:
        st.session_state.search_result = None


def is_verified_brand(value: object) -> bool:
    """Exclude empty and generated brand names such as 'Brand 17'."""

    brand_name = str(value).strip()
    return bool(brand_name) and not PLACEHOLDER_BRAND.fullmatch(brand_name)


def search_database(question: str) -> SearchResult:
    """Run the application's single database search flow."""

    medicine = search_anything(question)

    if medicine is None:
        return SearchResult(medicine=None)

    brands = get_brand_list(medicine)

    if brands is None or brands.empty:
        brand_name = medicine["brand"].get("Brand_Name", "")
        brand_names = (
            (str(brand_name).strip(),)
            if is_verified_brand(brand_name)
            else ()
        )
        return SearchResult(
            medicine=medicine,
            brand_names=brand_names,
        )

    # Preserve database order while removing duplicates and placeholders.
    brand_names = tuple(
        dict.fromkeys(
            str(name).strip()
            for name in brands["Brand_Name"].tolist()
            if is_verified_brand(name)
        )
    )

    return SearchResult(
        medicine=medicine,
        brand_names=brand_names,
    )


def resolve_medicine(
    database: PharmaDatabase,
    result: SearchResult,
    selected_brand: str,
) -> dict[str, Any] | None:
    """Resolve the selected brand to a complete medicine record."""

    if result.medicine is None:
        return None

    matched_brand = str(
        result.medicine["brand"].get("Brand_Name", "")
    ).strip()

    if selected_brand == matched_brand:
        return result.medicine

    return database.get_complete_medicine(selected_brand)


def clean_value(record: Any, field: str) -> str:
    """Convert a database field into clean prompt text."""

    value = record.get(field, "")

    if value is None:
        return ""

    text = str(value).strip()
    return "" if text.lower() == "nan" else text


def build_ai_context(medicine: dict[str, Any] | None) -> str:
    """Create structured medicine context for the AI engine."""

    if medicine is None:
        return NOT_FOUND_CONTEXT

    brand = medicine["brand"]
    generic = medicine["generic"]
    company = medicine["company"]
    product = medicine["product"]

    fields = (
        ("Brand Name", clean_value(brand, "Brand_Name")),
        ("Generic Name", clean_value(generic, "Generic_Name")),
        (
            "Gujarati Name",
            clean_value(generic, "Generic_Name_Gujarati"),
        ),
        ("Strength", clean_value(brand, "Strength")),
        ("Dosage Form", clean_value(brand, "Dosage_Form")),
        ("Company", clean_value(company, "Company_Name")),
        ("Country", clean_value(company, "Country")),
        ("Pack Size", clean_value(product, "Pack_Size")),
        ("Schedule", clean_value(product, "Schedule")),
        ("GST", clean_value(product, "GST")),
    )

    return "\n".join(
        f"{label}: {value or 'Not available'}"
        for label, value in fields
    )

def render_brand_comparison(result: SearchResult) -> None:
    """Render side-by-side brand comparison when multiple brands exist."""

    if len(result.brand_names) < 2:
        return

    st.subheader("⚖️ Brand Comparison")

    column_left, column_right = st.columns(2)

    with column_left:
        brand_one = st.selectbox(
            "Select first brand",
            options=result.brand_names,
            index=0,
            key="comparison_brand_one",
        )

    with column_right:
        brand_two = st.selectbox(
            "Select second brand",
            options=result.brand_names,
            index=1,
            key="comparison_brand_two",
        )

    # Prevent comparing the same brand
    if brand_one == brand_two:
        st.warning("Please select two different brands.")
        return

    if st.button("Compare", key="compare_brands"):

        comparison = BrandComparison()

        comparison_result = comparison.compare_brands(
            brand_one,
            brand_two,
        )

        if not comparison_result["success"]:
            st.error(comparison_result["message"])
            return

        st.table(
            comparison.get_comparison_table(
                comparison_result,
            )
        )

        st.info(
            comparison.generate_summary(
                comparison_result,
            )
        )
def render_drug_interaction() -> None:
    """Render the Drug Interaction Checker UI."""

    st.subheader("💊 Drug Interaction Checker")

    medicine_one = st.text_input(
        "Medicine 1",
        key="interaction_medicine_1",
    )

    medicine_two = st.text_input(
        "Medicine 2",
        key="interaction_medicine_2",
    )

    if st.button("Check Interaction"):

        if not medicine_one.strip() or not medicine_two.strip():
            st.warning("Please enter both medicine names.")
            return

        interaction = DrugInteraction()

        with st.spinner("Checking drug interaction..."):
            result = interaction.check_interaction(
                medicine_one,
                medicine_two,
            )

        if not result["success"]:
            st.error(result["interaction"])
            return

        severity = result["severity"]
        if severity == "Major":
            st.error(f"**Severity:** {severity}")
        elif severity == "Moderate":
            st.warning(f"**Severity:** {severity}")
        else:
            st.success(f"**Severity:** {severity}")

        st.write("**Interaction:**", result["interaction"])
        st.write("**Mechanism:**", result["mechanism"])
        st.write("**Management:**", result["management"])
        st.write(
            "**Patient Counselling:**",
            result["patient_counselling"],
        )
def render_medicine_information(
    database: PharmaDatabase,
) -> None:
    """Render the single medicine-information section and card."""

    result = st.session_state.search_result

    if result is None:
        return

    st.subheader("💊 Medicine Information")

    if result.medicine is None:
        st.warning("Medicine not found in the database.")
        return

    if not result.brand_names:
        st.warning("No verified brand is available for this medicine.")
        return

    matched_brand = str(
        result.medicine["brand"]["Brand_Name"]
    ).strip()

    default_index = (
        result.brand_names.index(matched_brand)
        if matched_brand in result.brand_names
        else 0
    )

    # The application's only selectbox supports all matching brands.
    selected_brand = st.selectbox(
        "Select a brand",
        options=result.brand_names,
        index=default_index,
        key="selected_brand",
    )

    medicine = resolve_medicine(
        database,
        result,
        selected_brand,
    )

    if medicine is None:
        st.error("The selected brand could not be loaded.")
        return

    # The application's only medicine-card rendering path.
    show_medicine_card(medicine)
    
    render_brand_comparison(result)

def render_chat_history() -> None:
    """Render persisted chat messages in chronological order."""

    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])


def process_question(
    question: str,
    database: PharmaDatabase,
) -> None:
    """Search, call the AI engine, and persist the exchange."""

    clean_question = question.strip()

    if not clean_question:
        return

    result = search_database(clean_question)
    st.session_state.search_result = result

    # Clear the previous selection before brand options change.
    st.session_state.pop("selected_brand", None)

    medicine = result.medicine

    if medicine is not None and result.brand_names:
        matched_brand = str(
            medicine["brand"]["Brand_Name"]
        ).strip()

        selected_brand = (
            matched_brand
            if matched_brand in result.brand_names
            else result.brand_names[0]
        )

        medicine = resolve_medicine(
            database,
            result,
            selected_brand,
        )

    st.session_state.messages.append(
        {
            "role": "user",
            "content": clean_question,
        }
    )

    with st.spinner(
        "Clinical pharmacist is preparing a response..."
    ):
        response = ask_ai(
            clean_question,
            build_ai_context(medicine),
        )

    st.session_state.messages.append(
        {
            "role": "assistant",
            "content": response,
        }
    )

def main() -> None:
    """Compose and run the Pharma AI application."""

    load_dotenv()
    configure_app()
    initialize_session()

    database = get_database()

    st.title("💊 Pharma AI")
    st.caption("AI Clinical Pharmacy Assistant")

    render_medicine_information(database)
    
    def render_drug_interaction() -> None:
     """Render the Drug Interaction Checker."""

    st.subheader("💊 Drug Interaction Checker")

    medicine_one = st.text_input(
        "Medicine 1",
        key="interaction_medicine_one",
        placeholder="Example: Dolo 650",
    )

    medicine_two = st.text_input(
        "Medicine 2",
        key="interaction_medicine_two",
        placeholder="Example: Augmentin 625",
    )

    if st.button(
        "🔍 Check Interaction",
        key="check_interaction",
    ):

        if not medicine_one.strip() or not medicine_two.strip():
            st.warning("Please enter both medicine names.")
            return
        st.write("Reached Interaction")

        checker = DrugInteraction()
        
        result = checker.check_interaction(
            medicine_one,
            medicine_two,
        )
        st.write("After function")
        st.write(result)

        if not result["success"]:
            st.error(result["interaction"])
            return

        severity = result["severity"]

        if severity == "Major":
            st.error(f"🔴 Severity : {severity}")

        elif severity == "Moderate":
            st.warning(f"🟡 Severity : {severity}")

        elif severity == "Minor":
            st.info(f"🟢 Severity : {severity}")

        else:
            st.success(f"✅ {severity}")

        st.markdown("### ⚠ Interaction")
        st.write(result["interaction"])

        st.markdown("### ⚙ Mechanism")
        st.write(result["mechanism"])

        st.markdown("### 🩺 Management")
        st.write(result["management"])

        st.markdown("### 👨‍⚕️ Patient Counselling")
        st.write(result["patient_counselling"])

    if st.session_state.search_result is not None:
        st.divider()

    st.subheader("🤖 AI Clinical Pharmacist")
    render_chat_history()

    question = st.chat_input("દવા વિશે પ્રશ્ન પૂછો...")

    if question:
        process_question(question, database)
        st.rerun()


if __name__ == "__main__":
    main()