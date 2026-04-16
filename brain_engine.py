import google.generativeai as genai
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

class GaiaEngine:
    def __init__(self):
        self.model = genai.GenerativeModel('gemini-1.5-flash')

    def generate_code(self, prompt, context="Roblox Luau"):
        full_prompt = f"Atue como o melhor desenvolvedor do mundo. O usuário quer um script para {context}: {prompt}. Retorne APENAS o código puro."
        response = self.model.generate_content(full_prompt)
        return response.text
