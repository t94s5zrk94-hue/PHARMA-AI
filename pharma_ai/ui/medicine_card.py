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
    atc = medicine.get("atc", {})
    therapeutic = medicine.get("therapeutic", {})
    pharmacological = medicine.get("pharmacological", {})

    display_name = (
    medicine.get("display_name")
    or product.get("Product_Name")
    or brand.get("Brand_Name")
    or generic.get("Generic_Name")
    or "Unknown Product"
    )

    st.subheader(f"💊 {display_name}")
    
    tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs(
    ["💊 General","🧬 Generic","🏢 Company","🧾 ATC","🩺 Therapeutic","⚙️ Pharmacological",]
    )

    # -------------------------
    # General
    # -------------------------
    with tab1:
        safe_metric("Medicine", product, "Product_Name")
        safe_metric("Strength", brand, "Strength")
        safe_metric("Dosage Form", brand, "Dosage_Form")
        safe_metric("Pack Size", product, "Pack_Size")
        safe_metric("Schedule", product, "Schedule")

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
    # -------------------------
    # ATC
    # -------------------------
    with tab4:
        safe_metric("ATC Code", atc, "ATC_Code")
        safe_metric("ATC Name", atc, "ATC_Name")
        safe_metric("WHO Version", atc, "WHO_Version")
        safe_metric("Status", atc, "Status")    

    # -------------------------
    # Therapeutic
    # -------------------------
    with tab5:
        safe_metric("Therapeutic Class",therapeutic,"Therapeutic_Class_Name",)
        safe_metric("Description",therapeutic,"Description",)
        safe_metric("WHO Reference",therapeutic,"WHO_Reference",)
        safe_metric("Status",therapeutic,"Status",)  
    
        # -------------------------
        # Pharmacological
        # -------------------------
    with tab6:
        safe_metric("Pharmacological Class",pharmacological,"Pharmacological_Class_Name",)
        safe_metric("Description",pharmacological,"Description",)
        safe_metric("WHO Reference",pharmacological,"WHO_Reference",)
        safe_metric("Status",pharmacological,"Status",)