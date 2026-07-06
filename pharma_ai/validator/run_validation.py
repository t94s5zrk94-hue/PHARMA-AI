import os
import logging
import sys

# પ્રોજેક્ટ રૂટને પાથમાં ઉમેરે છે જેથી મોડ્યુલ ઈમ્પોર્ટમાં ભૂલ ન આવે
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pharma_ai.validator.database_validator import run_db_regression
from pharma_ai.validator.clinical_validator import run_clinical_regression

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    """
    Pharma AI: Master Validation Launcher
    આ ફંક્શન સમગ્ર સિસ્ટમનું ક્લિનિકલ અને ડેટાબેઝ વેલિડેશન કરે છે.
    """
    # પ્રોજેક્ટ રૂટ અને ડેટાબેઝ ડિરેક્ટરી સેટઅપ
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    DB_DIR = os.path.join(BASE_DIR, "database")

    logger.info("=== 🚀 PHARMA AI: STARTING FULL SYSTEM VALIDATION ===")
    
    # 1. Run Database Health Checks
    logger.info("Step 1: Running Database Regression...")
    db_results = run_db_regression()
    
    # 2. Run Clinical Interaction Suite
    logger.info("Step 2: Running Clinical Regression...")
    clinical_results = run_clinical_regression(DB_DIR)
    
    # Final Summary Output
    logger.info("=== ✅ VALIDATION COMPLETE ===")
    logger.info(f"Database Report: {db_results}")
    logger.info(f"Clinical Report: {clinical_results}")

if __name__ == "__main__":
    main()