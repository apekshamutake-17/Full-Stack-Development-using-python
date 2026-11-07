from flask import Flask
import platform

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to System Information"

@app.route("/info")
def info():
    return "System: " + platform.system() + "<br>Python Version: " + platform.python_version()

app.run()