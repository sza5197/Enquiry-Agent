from flask import Flask, render_template, request
import database
import ai_service
import business_rules
import actions

app = Flask(__name__)

database.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    message = request.form["message"]
    enquiry_id = database.save_enquiry(message)
    database.add_message(enquiry_id, "customer", message)   # ← log it as the first message

    extracted = ai_service.extract_enquiry(message)

    # The AI's proposal (what it thinks should happen)
    ai_proposed = extracted.get("proposed_action")
    ai_reason = extracted.get("reason")

    # Python's final decision (the authority)
    missing = business_rules.find_missing_fields(extracted)
    final_action, final_reason = business_rules.authorise_action(ai_proposed, extracted)

    # Execute the FINAL action Python decided on
    if final_action == "CREATE_JOB_REQUEST":
        result = actions.create_job_request(enquiry_id, extracted)
    elif final_action == "ASK_FOR_MISSING_INFORMATION":
        result = actions.ask_for_missing_information(enquiry_id, extracted, missing)
    else:
        result = actions.mark_for_human_review(enquiry_id, extracted, final_reason)

    return render_template(
        "result.html",
        enquiry_id=enquiry_id,
        message=message,
        extracted=extracted,
        missing=missing,
        ai_proposed=ai_proposed,
        ai_reason=ai_reason,
        final_action=final_action,
        final_reason=final_reason,
        result=result
    )


@app.route("/followup", methods=["POST"])
def followup():
    # NOTE (prototype): we trust enquiry_id from the form. In a real system we'd
    # verify the logged-in user is actually allowed to update this enquiry.
    enquiry_id = int(request.form["enquiry_id"])
    answer = request.form["answer"]

    # 1. log the customer's answer as a new message in the conversation
    database.add_message(enquiry_id, "customer", answer)

    # 2. read the whole conversation history for this enquiry
    messages = database.get_messages(enquiry_id)

    # 3. build a labelled conversation string the AI can understand
    conversation_lines = []
    for m in messages:
        who = "Customer" if m["sender"] == "customer" else "System"
        conversation_lines.append(f'{who}: "{m["text"]}"')
    conversation = "\n".join(conversation_lines)

    # 4. re-extract with the fuller context
    extracted = ai_service.extract_with_followup(conversation)

    ai_proposed = extracted.get("proposed_action")
    ai_reason = extracted.get("reason")

    # 5. Python authorises (final say)
    missing = business_rules.find_missing_fields(extracted)
    final_action, final_reason = business_rules.authorise_action(ai_proposed, extracted)

    # 6. execute the final action
    if final_action == "CREATE_JOB_REQUEST":
        result = actions.create_job_request(enquiry_id, extracted)
    elif final_action == "ASK_FOR_MISSING_INFORMATION":
        result = actions.ask_for_missing_information(enquiry_id, extracted, missing)
        # log the new follow-up question too, so the conversation stays complete
        for q in result["questions"]:
            database.add_message(enquiry_id, "system", q)
    else:
        result = actions.mark_for_human_review(enquiry_id, extracted, final_reason)

    # 7. get the original message to show at the top
    enquiry = database.get_enquiry(enquiry_id)

    return render_template(
        "result.html",
        enquiry_id=enquiry_id,
        message=enquiry["raw_message"],
        extracted=extracted,
        missing=missing,
        ai_proposed=ai_proposed,
        ai_reason=ai_reason,
        final_action=final_action,
        final_reason=final_reason,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)