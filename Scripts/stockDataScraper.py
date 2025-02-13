import yfinance as yf
import json
import time
import random
from pymongo import MongoClient

# Define MongoDB Atlas connection
MONGO_URI = "mongodb+srv://chrisbushelman:i7wPfB8sRMNlsCQT@cluster0.0gkw8.mongodb.net/"
mongo = MongoClient(MONGO_URI)
db = mongo['Project_3']  # Use your actual database name

# Define the companies
usCompanies = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "META", "TSLA", "AVGO", "ORCL", "CRM"]
foreignCompanies = ["TSM", "SSNLF", "ASML", "TCEHY", "BABA", "SAP", "SONY", "SOBKY", "INFY", "BIDU"]

# Define the date ranges for Trump and Biden
date_ranges = {
    "Trump": ("2017-01-20", "2017-12-31"),
    "Biden": ("2021-01-20", "2021-12-31")
}

def fetch_ticker_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for the given ticker within the specified date range.
    Returns a list of dictionaries with "Date" and "Close" prices.
    """
    stock = yf.Ticker(ticker)
    try:
        hist = stock.history(start=start_date, end=end_date)
        hist.index = hist.index.strftime('%Y-%m-%d')  # Convert dates to string format
        return [{"Date": date, "Close": row["Close"]} for date, row in hist.iterrows()]
    except Exception as e:
        print(f"Error fetching data for {ticker} from {start_date} to {end_date}: {e}")
        return []

def fetch_company_info(ticker):
    """
    Fetches company information such as name and address.
    """
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        return {
            "Company Name": info.get("shortName", ticker),
            "Address": info.get("address1", "Unknown"),
            "City": info.get("city", "Unknown"),
            "State": info.get("state", "Unknown"),
            "Country": info.get("country", "Unknown")
        }
    except Exception as e:
        print(f"Error fetching info for {ticker}: {e}")
        return {
            "Company Name": ticker,
            "Address": "Unknown",
            "City": "Unknown",
            "State": "Unknown",
            "Country": "Unknown"
        }

def push_to_mongo(data, collection_name):
    collection = db[collection_name]
    collection.delete_many({})  # Clear previous data before inserting new data
    collection.insert_one(data)
    print(f"Data successfully inserted into {collection_name}")

def main():
    all_tickers = usCompanies + foreignCompanies
    data_by_president = {"Trump": {}, "Biden": {}}  # Store data in dictionary format

    for ticker in all_tickers:
        print(f"\nProcessing ticker: {ticker}")
        company_info = fetch_company_info(ticker)  # Fetch company name and address

        for president, (start_date, end_date) in date_ranges.items():
            print(f"Fetching data for {company_info['Company Name']} ({ticker}) during {president}'s term")
            historical_data = fetch_ticker_data(ticker, start_date, end_date)

            if historical_data:
                data_by_president[president][ticker] = {
                    **company_info,  # Add company name and address info
                    "Date Range": f"{start_date} to {end_date}",
                    "Stock Data": historical_data
                }
            
            time.sleep(random.randint(3,5))  # Sleep to avoid rate limiting

    # Store all tickers inside a single document per presidency and push to MongoDB Atlas
    push_to_mongo(data_by_president["Trump"], "Trump_Presidency")
    push_to_mongo(data_by_president["Biden"], "Biden_Presidency")
    
    print("Data saved to MongoDB Atlas")

if __name__ == "__main__":
    main()

