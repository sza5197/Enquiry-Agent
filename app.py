from flask import Flask, render_template, request
import database
import ai_service
import business_rules

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

    return render_template(
        "result.html",
        enquiry_id=enquiry_id,
        message=message,
        extracted=extracted,
        missing=missing,
        status=status
    )


if __name__ == "__main__":
    app.run(debug=True)