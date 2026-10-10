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