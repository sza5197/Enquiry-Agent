import database

def ask_for_missing_information(enquiry_id, extacted, missing):
    questions = {
        "contact_information": "Could you please provide a phone number or email so we can reach you?",
        "suburb": "Which suburb are you located in?",
        "issue_summary": "Could you describe the problem you're having?",
    }

    asks = []
    for field in missing:
        asks.append(questions.get(field, f"Could you provide your {field}?"))

    return {
        "action": "ASK_FOR_MISSING_INFORMATION",
        "questions": asks,
    }



def create_job_request(enquiry_id, extracted):
    job_id = database.save_job_request(enquiry_id, extracted)

    return {
        "action": "CREATE_JOB_REQUEST",
        "job_id": job_id,
    }



def mark_for_human_review(enquiry_id, extracted, reason="Needs a human to review."):
    return {
        "action": "HUMAN_REVIEW",
        "reason": reason,
    }

