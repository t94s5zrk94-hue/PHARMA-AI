import os
import logging
from dotenv import load_dotenv
from google import genai

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

load_dotenv()

def get_client():
    """Returns the GenAI client initialized with the API key."""
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        logger.error("GEMINI_API_KEY is not set in the environment variables.")
        return None
    return genai.Client(api_key=api_key)

def ask_ai(question, medicine_database):
    client = get_client()
    if not client:
        return "### ⚠️ API કી સેટ કરેલી નથી."

    prompt = f"""
You are an experienced Clinical Pharmacist.
Respond ONLY in Gujarati.
The response must always follow this format.

💊 દવાનું નામ
🧬 Generic Name
✅ ઉપયોગ
⚙️ દવા કેવી રીતે કાર્ય કરે છે?
💊 સામાન્ય માત્રા (General educational information only)
⚠️ સામાન્ય આડઅસરો
🚫 ક્યારે સાવચેતી રાખવી?
🤰 ગર્ભાવસ્થા
🤱 સ્તનપાન
🧑‍⚕️ દર્દી માટે સલાહ
📚 મહત્વપૂર્ણ નોંધ

Rules:
• Use simple Gujarati.
• Use bullet points.
• Never diagnose diseases.
• Never prescribe medicines.
• Never recommend a dose for a specific patient.

Medicine Database:
{medicine_database}

User Question:
{question}
"""
    try:
        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )
        return response.text
    except Exception as e:
        logger.error(f"AI Call failed: {e}")
        return "### ⚠️ AI સેવા હાલમાં ઉપલબ્ધ નથી."

# --- Testing Block ---
if __name__ == "__main__":
    print("--- Testing PHARMA AI Engine ---")
    demo_db = "Generic Name: Paracetamol | Uses: Fever, Pain | Safety: Safe"
    demo_q = "Paracetamol શા માટે વપરાય છે?"
    
    result = ask_ai(demo_q, demo_db)
    print("\nAI Response:\n")
    print(result)