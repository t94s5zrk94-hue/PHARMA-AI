import streamlit as st

def safe_metric(label, data, key):
    """Utility to display metric only if the key exists and has value."""
    value = data.get(key)
    if value and value != "N/A" and str(value).strip().lower() != "nan":
        st.metric(label, value)

def show_medicine_card(medicine):

    if medicine is None:
        st.error("❌ Medicine Not Found")
        return
    
    
    product = medicine.get("product", {})
    brand = medicine.get("brand", {})
    generic = medicine.get("generic", {})
    company = medicine.get("company", {})

    display_name = (
    medicine.get("display_name")
    or product.get("Product_Name")
    or brand.get("Brand_Name")
    or generic.get("Generic_Name")
    or "Unknown Product"
)

    st.subheader(f"💊 {display_name}")

    tab1, tab2, tab3 = st.tabs(["💊 General", "🧬 Generic", "🏢 Company"])

    # -------------------------
    # General
    # -------------------------
    with tab1:
        safe_metric("Medicine", product, "Product_Name")
        safe_metric("Strength", brand, "Strength")
        safe_metric("Dosage Form", brand, "Dosage_Form")
        safe_metric("Pack Size", product, "Pack_Size")
        safe_metric("Schedule", product, "Schedule")
        safe_metric("GST", product, "GST")

    # -------------------------
    # Generic
    # -------------------------
    with tab2:
        safe_metric("Generic Name", generic, "Generic_Name")
        safe_metric("Gujarati Name", generic, "Generic_Name_Gujarati")
        safe_metric("Therapeutic Class", generic, "Therapeutic_Class")
        safe_metric("Available Strengths", generic, "Available_Strengths")
        safe_metric("Rx / OTC", generic, "Rx_OTC")

    # -------------------------
    # Company
    # -------------------------
    with tab3:
        safe_metric("Company", company, "Company_Name")
        safe_metric("Country", company, "Country")
        safe_metric("WHO GMP", company, "WHO_GMP")
        safe_metric("USFDA", company, "USFDA_Approved")
        safe_metric("Status", company, "Status")