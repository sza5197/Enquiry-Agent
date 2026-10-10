import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))


def ask_ai(message):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message
    )
    return response.text

print(ask_ai("Say hello in one short sentence."))