import streamlit as st


def show_medicine_card(medicine):

    if medicine is None:
        st.error("❌ Medicine Not Found")
        return

    product = medicine["product"]
    brand = medicine["brand"]
    generic = medicine["generic"]
    company = medicine["company"]

    st.subheader(f"💊 {product['Product_Name']}")

    tab1, tab2, tab3 = st.tabs(
        [
            "💊 General",
            "🧬 Generic",
            "🏢 Company"
        ]
    )

    # -------------------------
    # General
    # -------------------------
    with tab1:

        st.metric("Medicine", product["Product_Name"])
        st.metric("Strength", brand["Strength"])
        st.metric("Dosage Form", brand["Dosage_Form"])
        st.metric("Pack Size", product["Pack_Size"])
        st.metric("Schedule", product["Schedule"])
        st.metric("GST", product["GST"])

    # -------------------------
    # Generic
    # -------------------------
    with tab2:

        st.metric("Generic Name", generic["Generic_Name"])
        st.metric("Gujarati Name", generic["Generic_Name_Gujarati"])
        st.metric("Therapeutic Class", generic["Therapeutic_Class"])
        st.metric("Available Strengths", generic["Available_Strengths"])
        st.metric("Rx / OTC", generic["Rx_OTC"])

    # -------------------------
    # Company
    # -------------------------
    with tab3:

        st.metric("Company", company["Company_Name"])
        st.metric("Country", company["Country"])
        st.metric("WHO GMP", company["WHO_GMP"])
        st.metric("USFDA", company["USFDA_Approved"])
        st.metric("Status", company["Status"])