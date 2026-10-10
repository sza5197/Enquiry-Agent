import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-3.8-flash"

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

ENQUIRY_SCHEMA = {
    "type": "object",
    "properties": {
        "customer_name": {"type": "string", "nullable": True},
        "contact_information": {"type": "string", "nullable": True},
        "suburb": {"type": "string", "nullable": True},
        "issue_summary": {"type": "string", "nullable": True},
        "service_type": {"type": "string", "nullable": True},
        "urgency": {"type": "string", "enum": ["low", "normal", "high"]},
        "preferred_time": {"type": "string", "nullable": True},
    },
    "required": ["urgency"],
}


def extract_enquiry(message):
    prompt = f"""
You are an enquiry processor for a home-services business (HVAC, plumbing, electrical).
Read the customer message and extract the requested fields.

Rules:
- If a field is not present in the message, use null.
- Do not invent information that isn't there.

Customer message:
"{message}"
"""
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=prompt,
        config=types.GenerateContentConfig(
            response_mime_type="application/json",
            response_schema=ENQUIRY_SCHEMA,
        ),
    )

    raw_text = response.text
    data = json.loads(raw_text)
    return data


def ask_ai(message):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message
    )
    return response.text


print(extract_enquiry("yo my heaters making a mad rattling noise and wont heat, im in tarneit"))
