import os
import json
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

MODEL_NAME = "gemini-flash-lite-latest"

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
        "proposed_action": {
            "type": "string",
            "enum": ["CREATE_JOB_REQUEST", "ASK_FOR_MISSING_INFORMATION", "HUMAN_REVIEW"]
        },
        "reason": {"type": "string"},
    },
    "required": ["urgency"],
}


def extract_enquiry(message):
    prompt = f"""
You are an enquiry processor for a home-services business (HVAC, plumbing, electrical).
Read the customer message and extract the requested fields.

Extraction rules:
- If a field is not present in the message, use null.
- Do not invent information that isn't there.

Propose ONE action from these three:
- CREATE_JOB_REQUEST: the message is a genuine, in-scope service request with enough detail to act on.
- ASK_FOR_MISSING_INFORMATION: it's a real service request but important details are missing.
- HUMAN_REVIEW: the message is out of scope (not a home-services job), contradictory, unclear, or something a human should look at.

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


