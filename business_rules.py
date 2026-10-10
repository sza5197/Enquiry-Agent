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


# a complete enquiry (all three present)
complete = {
    "issue_summary": "Aircon not cooling",
    "suburb": "Werribee",
    "contact_information": "0412 345 678"
}

# an incomplete one (no contact)
incomplete = {
    "issue_summary": "Heater rattling",
    "suburb": "Tarneit",
    "contact_information": None
}

print("Complete enquiry:")
print("  missing:", find_missing_fields(complete))
print("  status:", determine_status(complete))

print("Incomplete enquiry:")
print("  missing:", find_missing_fields(incomplete))
print("  status:", determine_status(incomplete))