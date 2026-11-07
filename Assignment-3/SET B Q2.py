from flask import Flask
from datetime import date

app = Flask(__name__)

@app.route("/")
def home():
    return "Happy Birthday! Today's Date: " + str(date.today())

app.run(debug=True)