import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)


def ask_ai(question, medicine_database):

    prompt = f"""
You are an experienced Clinical Pharmacist.

Respond ONLY in Gujarati.

The response must always follow this format.

💊 દવાનું નામ

🧬 Generic Name

✅ ઉપયોગ

⚙️ દવા કેવી રીતે કાર્ય કરે છે?

💊 સામાન્ય માત્રા
(General educational information only)

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

Medicine Database

{medicine_database}

User Question

{question}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        return response.text

    except Exception:

        return """
### ⚠️ AI સેવા હાલમાં ઉપલબ્ધ નથી

સંભવિત કારણો:

• Gemini API quota પૂર્ણ થઈ ગઈ છે.
• Internet Connection ઉપલબ્ધ નથી.
• Gemini Server વ્યસ્ત છે.

✅ Database માહિતી સફળતાપૂર્વક ઉપલબ્ધ છે.
"""