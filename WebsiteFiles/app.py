from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd
import json



app = Flask(__name__)

# Attach Dash app to Flask
# create_dash_app(app)

@app.route("/")
def index():
    return render_template("index.html")


## app launcher
if __name__ == "__main__":
    app.run(debug=True)