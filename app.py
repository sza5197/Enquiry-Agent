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
    missing = business_rules.find_missing_fields(extracted)
    status = business_rules.determine_status(extracted)

    chosen = business_rules.selection_action(status)

    if chosen == "CREATE_JOB_REQUEST":
        result = actions.create_job_request(enquiry_id, extracted)

    elif chosen == "ASK_FOR_MISSING_INFORMATION":
        result = actions.ask_for_missing_information(enquiry_id, extracted, missing)

    else:
        result = actions.mark_for_human_review(enquiry_id, extracted)

    return render_template(
        "result.html",
        enquiry_id=enquiry_id,
        message=message,
        extracted=extracted,
        missing=missing,
        status=status,
        result=result
    )


if __name__ == "__main__":
    app.run(debug=True)