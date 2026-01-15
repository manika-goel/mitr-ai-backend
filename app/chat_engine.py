# import os
# from google import genai
# from dotenv import load_dotenv

# load_dotenv()

# client = genai.Client(
#     api_key=os.getenv("GEMINI_API_KEY"),
#     http_options={'api_version': 'v1beta'}
# )

# def get_mitrai_response(user_message):
#     try:
#         instruction = (
#             "Tumhara naam MitrAI hai. Tum ek empathetic dost ho. Hinglish mein baat karo. "
#             "Hamesha chote jawab do (sirf 2-3 lines). Zyada lambe paragraphs mat likho.Use friendly Hinglish(Hindi+English) like a friend.Don't give long lectures or bullet points unless asked.Ask only ONE follow-up question related to user's emotional state or well-being after your response to keep the conversation going.Koshish karo ki jawab 3-4 lines se zyada na ho, lekin hamesha apni baat poori karo.Don't give cut-off sentences."
#         )# Aapki list se uthaya gaya model: gemini-2.5-flash
#         response = client.models.generate_content(
#             model="gemini-2.5-flash", 
#             contents=user_message,
#             config={
#                 "system_instruction": instruction,
#                 "max_output_tokens": 500, # Ye response ki length ko zabardasti chota rakhega
#                 "temperature": 0.7
#             }
#         )
#         return response.text
#     except Exception as e:
#         print(f"Error Detail: {e}")
#         return (f"Dost, lagta hai network mein kuch gadbad hai. Phir se try karein? 💙")

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()

# OpenRouter Configuration
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY") # .env mein ye naam rakhiye
MODEL_NAME = "meta-llama/llama-3.3-70b-instruct:free"

def get_mitrai_response(user_message):
    try:
        instruction = (
            "Tumhara naam MitrAI hai. Tum ek empathetic dost ho. Hinglish mein baat karo. "
            "Hamesha chote jawab do (sirf 2-3 lines). Zyada lambe paragraphs mat likho. "
            "Use friendly Hinglish(Hindi+English) like a friend. Don't give long lectures "
            "or bullet points unless asked. Ask only ONE follow-up question related to "
            "user's emotional state or well-being after your response. Koshish karo ki "
            "jawab 3-4 lines se zyada na ho, lekin hamesha apni baat poori karo."
            "User se tum ya aap kehkar baat kro."
        )

        # OpenRouter API Call
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
            },
            data=json.dumps({
                "model": MODEL_NAME,
                "messages": [
                    {"role": "system", "content": instruction},
                    {"role": "user", "content": user_message}
                ],
                "temperature": 0.7,
                "max_tokens": 500
            })
        )

        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            print(f"API Error: {response.status_code} - {response.text}")
            return "Dost, lagta hai network mein kuch gadbad hai. Phir se try karein? 💙"

    except Exception as e:
        print(f"Error Detail: {e}")
        return "Dost, lagta hai network mein kuch gadbad hai. Phir se try karein? 💙"