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
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ENQUIRY_SCHEMA,
            ),
        )
        data = json.loads(response.text)
        return data

    except Exception as e:
        # If the AI call fails (API down, quota exceeded, bad response, etc.),
        # fall back safely: don't crash, don't guess — route to a human.
        print(f"[ai_service] extract_enquiry failed: {e}")
        return {
            "customer_name": None,
            "contact_information": None,
            "suburb": None,
            "issue_summary": None,
            "service_type": None,
            "urgency": "normal",
            "preferred_time": None,
            "proposed_action": "HUMAN_REVIEW",
            "reason": "The automated system could not process this enquiry, so it has been sent for human review.",
        }

    raw_text = response.text
    data = json.loads(raw_text)
    return data


def ask_ai(message):
    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=message
    )
    return response.text


def extract_with_followup(conversation):
    prompt = f"""
You are an enquiry processor for a home-services business (HVAC, plumbing, electrical).
Below is the conversation so far between the customer and the system.
Read ALL of it together and extract the current best understanding of the enquiry, then propose the next action.

Extraction rules:
- Combine information from the whole conversation.
- If a field is still not present anywhere in the conversation, use null.
- Do not invent information that isn't there.

Propose ONE action:
- CREATE_JOB_REQUEST: genuine, in-scope request with enough detail to act on.
- ASK_FOR_MISSING_INFORMATION: real request but important details still missing.
- HUMAN_REVIEW: out of scope, contradictory, or unclear.

Give a short reason for your proposed action.

Conversation so far:
{conversation}
"""
    try:
        response = client.models.generate_content(
            model=MODEL_NAME,
            contents=prompt,
            config=types.GenerateContentConfig(
                response_mime_type="application/json",
                response_schema=ENQUIRY_SCHEMA,
            ),
        )
        data = json.loads(response.text)
        return data

    except Exception as e:
        # If the AI call fails (API down, quota exceeded, bad response, etc.),
        # fall back safely: don't crash, don't guess — route to a human.
        print(f"[ai_service] extract_enquiry failed: {e}")
        return {
            "customer_name": None,
            "contact_information": None,
            "suburb": None,
            "issue_summary": None,
            "service_type": None,
            "urgency": "normal",
            "preferred_time": None,
            "proposed_action": "HUMAN_REVIEW",
            "reason": "The automated system could not process this enquiry, so it has been sent for human review.",
        }

    raw_text = response.text
    data = json.loads(raw_text)
    return data




