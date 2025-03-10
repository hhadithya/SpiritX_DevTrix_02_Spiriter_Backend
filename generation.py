import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(player_name: str, player_info: str):
    prompt = f"Here are the cricket stats of {player_name}: {player_info}. Format this information in a natural and engaging way."

    model = genai.GenerativeModel("gemini-1.5-pro")

    response = model.generate_content(prompt)
    
    try:
        return response.candidates[0].content.parts[0].text
    
    except (AttributeError, IndexError, KeyError) as e:
        return f"Error extracting text: {e}"