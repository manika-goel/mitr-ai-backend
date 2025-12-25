import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY"),
    http_options={'api_version': 'v1beta'}
)

def get_mitrai_response(user_message):
    try:
        instruction = (
            "Tumhara naam MitrAI hai. Tum ek empathetic dost ho. Hinglish mein baat karo. "
            "Hamesha chote jawab do (sirf 2-3 lines). Zyada lambe paragraphs mat likho.Use friendly Hinglish(Hindi+English) like a friend.Don't give long lectures or bullet points unless asked.Ask only ONE follow-up question related to user's emotional state or well-being after your response to keep the conversation going.Koshish karo ki jawab 3-4 lines se zyada na ho, lekin hamesha apni baat poori karo.Don't give cut-off sentences."
        )# Aapki list se uthaya gaya model: gemini-2.5-flash
        response = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=user_message,
            config={
                "system_instruction": instruction,
                "max_output_tokens": 500, # Ye response ki length ko zabardasti chota rakhega
                "temperature": 0.7
            }
        )
        return response.text
    except Exception as e:
        print(f"Error Detail: {e}")
        return (f"Dost, lagta hai network mein kuch gadbad hai. Phir se try karein? 💙")