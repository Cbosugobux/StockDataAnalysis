from flask import Flask, jsonify, render_template
from flask_pymongo import PyMongo
import pandas as pd
import json
import os

# Initialize Flask app
app = Flask(__name__)

# =====================[ MongoDB Connection ]=====================
# Connecting to the local MongoDB database named 'stockmarket_db'
app.config["MONGO_URI"] = "mongodb://localhost:27017/stockmarket_db"
mongo = PyMongo(app)

# =====================[ Page Routes - Rendering HTML ]=====================

@app.route("/")
def index():
    """ Renders the homepage. """
    return render_template("index.html")

@app.route("/about")
def about():
    """ Renders the About page. """
    return render_template("about.html")

@app.route("/stockData")
def stock_data():
    """ Renders the Stock Data page. """
    return render_template("stockData.html")

@app.route("/map")
def map_visualization():
    """ Renders the Map Visualization page. """
    return render_template("MapVisualization.html")

@app.route("/diversity")
def diversity_info():
    """ Renders the Diversity Information page. """
    return render_template("diversityinfo.html")

@app.route("/findings")
def findings():
    """ Renders the Findings page. """
    return render_template("findings.html")


# =====================[ API Routes - Serving Data ]=====================

@app.route("/api/stocks/<president>")
def get_stocks(president):
    """
    Fetches stock market data for a given presidency.
    
    Parameters:
        president (str): Either 'biden' or 'trump' to retrieve stock data.

    Returns:
        JSON object containing stock market data for the selected presidency.
    """
    if president.lower() == "biden":
        stocks_collection = mongo.db.Biden_Presidency
    elif president.lower() == "trump":
        stocks_collection = mongo.db.Trump_Presidency
    else:
        return jsonify({"error": "Invalid president name. Use 'biden' or 'trump'."}), 400
    
    # Retrieve stock data from MongoDB and return it as JSON
    stocks_data = list(stocks_collection.find({}, {"_id": 0}))  # Exclude MongoDB '_id' field
    return jsonify(stocks_data)


@app.route("/api/diversity")
def get_diversity():
    """
    Fetches employee diversity data from an Excel file.

    Returns:
        JSON object containing diversity data for 2017 and 2021.
    """
    # Define file path for the diversity dataset
    diversity_file = os.path.join(os.path.dirname(__file__), "diversityData", "Resources", "Employee Diversity.xlsx")


    try:
        # Read data from Excel sheets
        df_2017 = pd.read_excel(diversity_file, sheet_name="2017")
        df_2021 = pd.read_excel(diversity_file, sheet_name="2021")

        # Convert data to JSON format
        diversity_data = {
            "2017": df_2017.to_dict(orient="records"),
            "2021": df_2021.to_dict(orient="records")
        }
        return jsonify(diversity_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle file reading errors


@app.route("/api/map")
def get_map_data():
    """
    Fetches GeoJSON data for company locations.

    Returns:
        JSON object containing company location data.
    """
    try:
        with open("companyLocations.geojson", "r") as file:
            geojson_data = json.load(file)
        return jsonify(geojson_data)
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500  # Handle file read errors


# =====================[ Flask App Launcher ]=====================

if __name__ == "__main__":
    # Runs the Flask server in debug mode (useful for development)
    app.run(debug=True)
