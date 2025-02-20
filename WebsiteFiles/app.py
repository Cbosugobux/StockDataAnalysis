from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd
import json



app = Flask(__name__)

# Attach Dash app to Flask
# create_dash_app(app)

# ========= [MongoDB Connection] =========
app.config["MONGO_URI"] = "mongodb://localhost:27017/stockmarket_db"
mongo = PyMongo(app)

@app.route("/")
def index():
    return render_template("index.html")

# ========= [API: Stock Data] =========
@app.route("/api/stocks/<president>")
def get_stocks(president):
    if president.lower() == "biden":
        stocks_collection = mongo.db.Biden_Presidency
    elif president.lower() == "trump":
        stocks_collection = mongo.db.Trump_Presidency
    else:
        return jsonify({"error": "Invalid president name. Use 'biden' or 'trump'."}), 400
    
    stocks_data = list(stocks_collection.find({}, {"_id": 0}))  # Remove MongoDB's _id field
    return jsonify(stocks_data)


# ========= [API: Diversity Data] =========
@app.route("/api/diversity")
def get_diversity():
    df_2017 = pd.read_excel(r'C:\Users\Rob Jowaisas\Desktop\DataBootCamp\GitHubRepositories\Project3\Resources\Employee Diversity.xlsx', sheet_name='2017')
    df_2021 = pd.read_excel(r'C:\Users\Rob Jowaisas\Desktop\DataBootCamp\GitHubRepositories\Project3\Resources\Employee Diversity.xlsx', sheet_name='2021')

    
    diversity_data = {
        "2017": df_2017.to_dict(orient='records'),
        "2021": df_2021.to_dict(orient='records')
    }
    return jsonify(diversity_data)

# ========= [API: Map Data] =========
@app.route("/api/map")
def get_map_data():
    with open("companyLocations.geojson", "r") as file:
        geojson_data = json.load(file)
    return jsonify(geojson_data)

## app launcher
if __name__ == "__main__":
    app.run(debug=True)