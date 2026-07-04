import logging
# sys દૂર કર્યું (Unused)
from interaction import DrugInteraction # તમારા ફોલ્ડર સ્ટ્રક્ચર મુજબ adjust કરશો

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def main():
    print("===========================")
    print("      PHARMA AI CLI        ")
    print("===========================")
    
    try:
        checker = DrugInteraction()
    except Exception as e:
        logger.error(f"Initialization Error: {e}")
        return

    while True:
        try:
            med1 = input("\nપહેલી દવાનું નામ (અથવા 'exit'): ").strip()
            if med1.lower() == 'exit': break
            if not med1:
                print("ભૂલ: કૃપા કરીને પ્રથમ દવાનું નામ લખો.")
                continue
                
            med2 = input("બીજી દવાનું નામ (અથવા 'exit'): ").strip()
            if med2.lower() == 'exit': break
            if not med2:
                print("ભૂલ: કૃપા કરીને બીજી દવાનું નામ લખો.")
                continue
            
            logger.info(f"Analyzing interaction between {med1} and {med2}...")
            result = checker.check_interaction(med1, med2)
            
            if result['success']:
                print("-" * 40)
                print(f"Severity: {result['severity']}")
                print(f"Interaction: {result['interaction']}")
                print(f"Mechanism: {result['mechanism']}")
                print(f"Management: {result['management']}")
                print(f"Advice: {result['patient_counselling']}")
                print("-" * 40)
            else:
                print(f"Error: {result['interaction']}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! પ્રોગ્રામ બંધ થઈ રહ્યો છે...")
            break
        except Exception as e:
            logger.error(f"Unexpected Error: {e}")

if __name__ == "__main__":
    main()