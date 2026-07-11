import streamlit as st

def safe_metric(label, data, key):
    """Utility to display metric only if the key exists and has value."""
    value = data.get(key)
    if value and value != "N/A" and str(value).strip().lower() != "nan":
        st.metric(label, value)

def show_clinical_table(title: str, data: list, columns: list):
    """Displays clinical information in a consistent format."""

    st.subheader(title)

    if not data:
        st.info("No data available.")
        return

    import pandas as pd

    df = pd.DataFrame(data)

    available_columns = [col for col in columns if col in df.columns]

    st.dataframe(
        df[available_columns],
        use_container_width=True,
        hide_index=True,
    )

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
    
    tab1, tab2, tab3, tab4, tab5, tab6, \
    tab7, tab8, tab9, tab10, \
    tab11, tab12, tab13, tab14, \
    tab15, tab16 = st.tabs([
        "💊 General","🧬 Generic","🏢 Company","🧾 ATC","🩺 Therapeutic","⚙️ Pharmacological",
        "🔄 Interactions","⛔ Contraindications","⚠️ Warnings","🤒 Side Effects","🤰 Pregnancy",
        "👶 Lactation","🩸 Renal","🫀 Hepatic","🩺 Monitoring","📚 Evidence",])

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
    
    with tab7:
        show_clinical_table(
            "Drug Interactions",
            medicine.get("interaction", []),
            [
                "Generic_A",
                "Generic_B",
                "Severity",
                "Clinical_Effect",
                "Management",
            ],
        )

    with tab8:
        show_clinical_table(
            "Contraindications",
            medicine.get("contraindication", []),
            [
                "Contraindication",
                "Severity",
                "Recommendation",
            ],
        )

    with tab9:
        show_clinical_table(
            "Warnings",
            medicine.get("warning", []),
            [
                "Warning",
                "Severity",
                "Recommendation",
            ],
        )

    with tab10:
        show_clinical_table(
            "Side Effects",
            medicine.get("side_effect", []),
            [
                "Side_Effect",
                "Frequency",
                "Severity",
                "Action",
            ],
        )

    with tab11:
        show_clinical_table(
            "Pregnancy",
            medicine.get("pregnancy", []),
            [
                "Pregnancy_Risk",
                "Trimester",
                "Recommendation",
                "Clinical_Notes",
            ],
        )
    with tab12:
        show_clinical_table(
            "Lactation",
            medicine.get("lactation", []),
            [
                "Lactation_Risk",
                "Recommendation",
                "Clinical_Notes",
            ],
        )

    with tab13:
        show_clinical_table(
            "Renal Dose Adjustment",
            medicine.get("renal", []),
            [
                "Renal_Category",
                "eGFR_Min",
                "eGFR_Max",
                "Dose_Recommendation",
                "Clinical_Note",
            ],
        )

    with tab14:
        show_clinical_table(
            "Hepatic Dose Adjustment",
            medicine.get("hepatic", []),
            [
                "Hepatic_Category",
                "Child_Pugh_Class",
                "Dose_Recommendation",
                "Clinical_Note",
            ],
        )

    with tab15:
        show_clinical_table(
            "Monitoring Parameters",
            medicine.get("monitoring", []),
            [
                "Monitoring_Parameter",
                "Monitoring_Frequency",
                "Target_Range",
                "Clinical_Action",
            ],
        )

    with tab16:
        show_clinical_table(
            "Clinical Evidence",
            medicine.get("evidence", []),
            [
                "Clinical_Topic",
                "Evidence_Summary",
                "Evidence_Level",
                "Guideline_Source",
                "Reference_Year",
            ],
        )