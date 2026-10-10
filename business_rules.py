# The fields this business requires before a job can be created.
# Explicit on purpose (see project doc section 15): a clear problem,
# a location, and a way to contact the customer. Preferred time is optional.
REQUIRED_FIELDS = ["issue_summary", "suburb", "contact_information"]


def find_missing_fields(enquiry_data):
    missing = []
    for field in REQUIRED_FIELDS:
        value = enquiry_data.get(field)
        if value is None or value == "":
            missing.append(field)
    return missing


def determine_status(enquiry_data):
    missing = find_missing_fields(enquiry_data)
    if missing:
        return "INCOMPLETE"
    else:
        return "COMPLETE"


def selection_action(status):
    if status == "COMPLETE":
        return "CREATE_JOB_REQUEST"

    elif status == "INCOMPLETE":
        return "ASK_FOR_MISSING_INFORMATION"

    else:
        return "HUMAN_REVIEW"


def authorise_action(proposed_action, enquiry_data):
    missing = find_missing_fields(enquiry_data)

    # 1. If the AI flagged it for a human, trust that judgement.
    if proposed_action == "HUMAN_REVIEW":
        return "HUMAN_REVIEW", "AI flagged this for human review."

    # 2. If required fields are missing, Python forces ASK — no matter what the AI proposed.
    if missing:
        return "ASK_FOR_MISSING_INFORMATION", f"Required fields missing: {', '.join(missing)}."

    # 3. Nothing missing and not flagged → allow the job to be created.
    return "CREATE_JOB_REQUEST", "All required fields present and enquiry is in scope."


