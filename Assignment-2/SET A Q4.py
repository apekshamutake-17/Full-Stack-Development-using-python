from flask import Flask, request

app = Flask(__name__)

@app.route("/")
def home():
    return """
    <html>
    <body>
        <h1>Request-Response Cycle</h1>
        <form action="/submit" method="POST">
            <label>Enter Your Name:</label>
            <input type="text" name="name" required>
            <button type="submit">Submit</button>
        </form>
    </body>
    </html>
    """

@app.route("/submit", methods=["POST"])
def submit():
    name = request.form.get("name", "")
    return f"""
    <h1>Response Received Successfully!</h1>
    <p>Hello, {name}!</p>
    <a href="/">Go Back</a>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)