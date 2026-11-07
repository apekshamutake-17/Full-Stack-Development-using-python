# Create a Flask application displaying your name and roll number.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Name: Apeksha, Roll Number: 46"

if __name__ == '__main__':
    app.run(debug=True)