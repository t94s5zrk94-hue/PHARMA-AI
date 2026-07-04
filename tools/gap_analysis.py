import pandas as pd
import logging

logger = logging.getLogger(__name__)

def perform_clinical_gap_analysis():
    file_path = 'database/medicine/generic_master.csv'
    
    try:
        df = pd.read_csv(file_path)
    except FileNotFoundError:
        logger.error(f"File not found at {file_path}")
        return None

    clinical_fields = [
        'Pregnancy_Safety', 'Lactation_Safety', 'Renal_Adjustment', 
        'Hepatic_Adjustment', 'Contraindications', 'ATC_Code', 
        'Common_Side_Effects', 'Serious_Side_Effects'
    ]
    critical_fields = ['ATC_Code', 'Pregnancy_Safety', 'Contraindications']

    total_generics = len(df)
    missing_stats = {}
    
    # Filter available fields to prevent KeyErrors
    available_fields = [f for f in clinical_fields if f in df.columns]
    checked_fields_count = len(available_fields)

    for field in available_fields:
        missing_mask = (
            df[field].isna() | 
            df[field].astype(str).str.strip().eq("") | 
            df[field].astype(str).str.strip().eq("Unknown")
        )
        missing_stats[field] = missing_mask.sum()

    # Completion calculation with zero-check
    total_cells = total_generics * checked_fields_count
    total_missing = sum(missing_stats.values())
    completion = ((total_cells - total_missing) / total_cells) * 100 if total_cells > 0 else 0
    
    # Critical Records identification
    available_critical = [c for c in critical_fields if c in df.columns]
    critical_df = df[df[available_critical].isna().any(axis=1) | df[available_critical].eq("Unknown").any(axis=1)]
    critical_df.to_csv('database/medicine/critical_missing_report.csv', index=False)

    # Console Output
    print("============================================")
    print("      PHARMA AI DATA QUALITY DASHBOARD      ")
    print("============================================")
    print(f"Total Generics : {total_generics}")
    for field, count in missing_stats.items():
        print(f"{field.ljust(22)} : {count} missing")
    print("-" * 44)
    print(f"✔ Report Generated Successfully")
    print(f"✔ Overall Completion : {completion:.2f}%")
    print(f"✔ Critical Missing Records : {len(critical_df)}")
    print("============================================")

    return {
        "total_generics": total_generics,
        "completion": completion,
        "missing_stats": missing_stats,
        "critical_records": len(critical_df)
    }

if __name__ == "__main__":
    perform_clinical_gap_analysis()