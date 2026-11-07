# Display student information stored in dictionary.

from flask import Flask

app = Flask(__name__)

@app.route("/")
def student_info():
    student = {
        "name": "Apeksha Mutake",
        "rollno": "46",
        "age" : 20,
        "class" : "S.Y.Bsc(CS)"
    }

    return f"""
    <h2>Student Information</h2>
    Name: {student['name']}<br>
    Roll Number: {student['rollno']}<br>
    Age: {student['age']}<br>
    Class: {student['class']}<br>
   
    """

if __name__ == "__main__":
    app.run(debug=True)