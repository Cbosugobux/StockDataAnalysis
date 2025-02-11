import yfinance as yf
import json
import time
from datetime import datetime

# Define the companies and dates
usCompanies = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "META", "TSLA", "AVGO", "ORCL", "CRM"]
foreigncompanies = ["TSM", "SSNLF", "ASML", "TCEHY", "BABA", "SAP", "SONY", "SOBKY", "INFY", "BIDU"]

date_ranges = [
    ("2017-01-20", "2017-12-31"),
    ("2021-01-20", "2021-12-31")
]

# Function to convert DataFrame to dictionary with string keys
def df_to_dict_with_str_keys(df):
    """ Convert DataFrame to a dictionary with string keys. """
    return {str(k): v for k, v in df.to_dict().items()}

# Function to fetch stock data
def fetch_stock_data(tickers, start_date, end_date):
    data = {}
    for ticker in tickers:
        try:
            stock = yf.Ticker(ticker)
            
            # Fetch historical prices and convert index to string
            hist = stock.history(start=start_date, end=end_date)
            hist.index = hist.index.strftime('%Y-%m-%d')  # Convert index (dates) to strings
            
            # Convert historical prices to dict and ensure all keys are strings
            historical_prices = {date: row.to_dict() for date, row in hist.iterrows()}

            # Fetch financials and statistics
            income_stmt = df_to_dict_with_str_keys(stock.financials) if not stock.financials.empty else {}
            balance_sheet = df_to_dict_with_str_keys(stock.balance_sheet) if not stock.balance_sheet.empty else {}
            stats = stock.info if stock.info else {}

            # Store data
            data[ticker] = {
                "historical_prices": historical_prices,  # Now fully converted to JSON-compatible dict
                "income_statement": income_stmt,
                "balance_sheet": balance_sheet,
                "statistics": stats
            }
            
            print(f"Fetched data for {ticker} ({start_date} to {end_date})")
            time.sleep(1)  # Prevent rate limiting
            
        except Exception as e:
            print(f"Error fetching {ticker}: {e}")

    return data

# Fetch data for both JSONs
usCompanies_json = {}
foreignCompanies_json = {}

for start_date, end_date in date_ranges:
    usCompanies_json[f"{start_date}_{end_date}"] = fetch_stock_data(usCompanies, start_date, end_date)
    foreignCompanies_json[f"{start_date}_{end_date}"] = fetch_stock_data(foreigncompanies, start_date, end_date)

# Save data to JSON files
with open("usCompanies.json", "w") as f:
    json.dump(usCompanies_json, f, indent=4)

with open("foreignCompanies.json", "w") as f:
    json.dump(foreignCompanies_json, f, indent=4)

print("Data extraction complete. JSON files saved.")
