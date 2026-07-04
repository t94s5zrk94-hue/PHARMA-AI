import pandas as pd
import os
import logging
import time

# Logger setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

# Rules Configuration (Priority based)
RULES = {
    'combination': {'keywords': ['+', ' and ', '/', 'plus'], 'confidence': 'High'},
    'device': {'keywords': ['monitor', 'thermometer', 'nebulizer', 'stool', 'support'], 'confidence': 'High'},
    'surgical': {'keywords': ['mask', 'gloves', 'bandage', 'gown', 'sheet', 'closure'], 'confidence': 'High'},
    'consumable': {'keywords': ['diaper', 'napkin', 'strip', 'swab', 'syringe', 'dressing'], 'confidence': 'High'}
}

def classify_product(name):
    if pd.isna(name) or str(name).strip() == "":
        return 'unclassified', 'Low', 'None', True
        
    name = str(name).lower()
    for cat, data in RULES.items():
        for kw in data['keywords']:
            if kw in name:
                return cat, data['confidence'], kw, False
    return 'generic', 'Needs Review', 'None', True

def run_classification():
    start_time = time.time()
    # તમારી અપલોડ કરેલી ફાઈલના પાથ મુજબ
    raw_path = 'database/raw/raw_data.csv'
    output_path = 'database/staging/classified_data.csv'
    review_path = 'database/staging/review_required.csv'
    
    try:
        if not os.path.exists(raw_path):
            raise FileNotFoundError(f"Raw data file not found at {raw_path}")
            
        df = pd.read_csv(raw_path)
        
        # તમારી ફાઈલની કોલમ 'Generic Name' છે, તેથી અહીં મેપિંગ કરીએ
        if 'Generic Name' in df.columns:
            df = df.rename(columns={'Generic Name': 'Product_Name'})
        elif 'Product_Name' not in df.columns:
            raise ValueError("Required column 'Generic Name' or 'Product_Name' missing!")

        os.makedirs('database/staging', exist_ok=True)
        
        results = []
        for _, row in df.iterrows():
            cat, conf, rule, needs_review = classify_product(row['Product_Name'])
            row_dict = row.to_dict()
            row_dict.update({
                'Mapped_Category': cat, 
                'Confidence': conf,
                'Matched_Rule': rule, 
                'Needs_Review': 'Yes' if needs_review else 'No',
                'Processing_Status': 'Classified'
            })
            results.append(row_dict)
        
        df_out = pd.DataFrame(results)
        
        # Save output
        df_out[df_out['Needs_Review'] == 'No'].to_csv(output_path, index=False, encoding='utf-8-sig')
        df_out[df_out['Needs_Review'] == 'Yes'].to_csv(review_path, index=False, encoding='utf-8-sig')
        
        exec_time = time.time() - start_time
        summary = df_out['Mapped_Category'].value_counts()
        
        logger.info("\n==================================")
        logger.info("CLASSIFICATION SUMMARY")
        logger.info("Total Records        : %d", len(df_out))
        logger.info("Execution Time       : %.2f sec", exec_time)
        logger.info("==================================\n%s", summary)

    except Exception as e:
        logger.exception("Pipeline failed: %s", e)

if __name__ == "__main__":
    run_classification()