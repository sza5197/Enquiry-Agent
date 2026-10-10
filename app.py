from flask import Flask, render_template, request
import database
import ai_service

app = Flask(__name__)

database.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    message = request.form["message"]
    enquiry_id = database.save_enquiry(message)
    ai_reply = ai_service.ask_ai(message)
    return f"Enquiry #{enquiry_id} saved. AI says: {ai_reply}"


if __name__ == "__main__":
    app.run(debug=True)