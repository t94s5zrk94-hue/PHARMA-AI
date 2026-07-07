import logging
from modules.interaction import DrugInteraction  # સુધારેલ ઇમ્પોર્ટ પાથ

# Logging setup
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

def main():
    print("===========================================")
    print("      PHARMA AI - ડિજિટલ ફાર્માસિસ્ટ        ")
    print("===========================================")
    print("બે દવાઓ વચ્ચેની આંતરક્રિયા (Interaction) તપાસો.\n")
    
    try:
        # DrugInteraction ક્લાસનું ઇનિશિયલાઇઝેશન
        checker = DrugInteraction()
    except Exception as e:
        logger.error(f"Initialization Error: સિસ્ટમ શરૂ કરવામાં ભૂલ - {e}")
        return

    while True:
        try:
            print("\n--- નવી તપાસ ---")
            med1 = input("પહેલી દવાનું નામ (અથવા 'exit'): ").strip()
            if med1.lower() == 'exit': break
            
            med2 = input("બીજી દવાનું નામ (અથવા 'exit'): ").strip()
            if med2.lower() == 'exit': break
            
            if not med1 or not med2:
                print("ભૂલ: કૃપા કરીને બંને દવાનું નામ લખો.")
                continue
            
            # વિશ્લેષણ
            logger.info(f"વિશ્લેષણ ચાલુ છે: {med1} અને {med2}...")
            result = checker.check_interaction(med1, med2)
            
            if result.get('success'):
                print("-" * 45)
                print(f"🔴 తీవ్రતા (Severity): {result.get('severity', 'N/A')}")
                print(f"💊 આંતરક્રિયા (Interaction): {result.get('interaction', 'N/A')}")
                print(f"⚙️ કેવી રીતે કાર્ય કરે છે?: {result.get('mechanism', 'N/A')}")
                print(f"🩺 વ્યવસ્થાપન (Management): {result.get('management', 'N/A')}")
                print(f"👨‍⚕️ દર્દી માટે સલાહ: {result.get('patient_counselling', 'N/A')}")
                print("-" * 45)
            else:
                print(f"સૂચના: {result.get('interaction', 'માહિતી ઉપલબ્ધ નથી.')}")
        
        except KeyboardInterrupt:
            print("\n\nGoodbye! પ્રોગ્રામ બંધ થઈ રહ્યો છે...")
            break
        except Exception as e:
            logger.error(f"અણધારી ભૂલ: {e}")

if __name__ == "__main__":
    main()