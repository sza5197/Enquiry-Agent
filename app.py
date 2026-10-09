from flask import Flask, render_template, request
import database

app = Flask(__name__)

database.init_db()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/submit", methods=["POST"])
def submit():
    message = request.form["message"]
    enquiry_id = database.save_enquiry(message)
    return f"You submitted (saved as enquiry #{enquiry_id}): {message}"


if __name__ == "__main__":
    app.run(debug=True)