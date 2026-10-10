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


if __name__ == "__main__":
    app.run(debug=True)