from flask import Flask, request

app = Flask(__name__)

students = ["Apeksha", "Priya", "Rahul", "Sneha", "Amit"]

@app.route("/", methods=["GET", "POST"])
def search():
    if request.method == "POST":
        name = request.form.get("name", "").strip()

        found_student = None

        for student in students:
            if student.lower() == name.lower():
                found_student = student
                break

        if found_student:
            result = f"Student Found: {found_student}"
        else:
            result = f"Student Not Found: {name}"

        return f"""
        <html>
        <body>
            <h1>Student Search Result</h1>
            <h2>{result}</h2>
            <a href="/">Search Again</a>
        </body>
        </html>
        """

    return """
    <html>
    <body>
        <h1>Student Search System</h1>
        <form method="POST">
            <label>Enter Student Name:</label>
            <input type="text" name="name" required>
            <button type="submit">Search</button>
        </form>
        </body>
    </html>
    """

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)