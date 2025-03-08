import os
from dotenv import load_dotenv
import google.generativeai as genai

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

def generate_response(query: str, player_info: str):
    prompt = (
        f"Answer this user query concisely: '{query}'.\n"
        f"Player data: {player_info}.\n"
        "If the data does not contain an exact answer, respond with 'I don't have enough details on that. Could you ask in another way?'"
    )
    model = genai.GenerativeModel("gemini-1.5-pro")

    response = model.generate_content(prompt)
    
    try:
        return response.candidates[0].content.parts[0].text
    
    except (AttributeError, IndexError, KeyError) as e:
        return f"Error extracting text: {e}"