from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return "Product App is Running"

@app.route("/product/<int:product_id>")
def product(product_id):
    return "Product ID: " + str(product_id) + "<br>Product Name: Laptop<br>Price: 50000"

app.run(port=5000)