import yfinance as yf
import json
import time

# Define the companies and date ranges
usCompanies = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "META", "TSLA", "AVGO", "ORCL", "CRM"]
foreignCompanies = ["TSM", "SSNLF", "ASML", "TCEHY", "BABA", "SAP", "SONY", "SOBKY", "INFY", "BIDU"]

# Define the date ranges for which to fetch data
date_ranges = [
    ("2017-01-20", "2017-12-31"),
    ("2021-01-20", "2021-12-31")
]

def fetch_ticker_data(ticker, date_ranges):
    """
    Fetch historical stock data for the given ticker over the specified date ranges.
    Only the closing price is retained for each day.
    Returns a dictionary with date range keys and a list of day-wise data dictionaries.
    Each day-wise dictionary includes:
        - "Date": the date as a string (YYYY-MM-DD)
        - "Close": the closing price for that day
    """
    ticker_data = {}
    stock = yf.Ticker(ticker)
    
    for start_date, end_date in date_ranges:
        try:
            # Fetch historical data for the given date range
            hist = stock.history(start=start_date, end=end_date)
            # Convert the index (dates) to string format
            hist.index = hist.index.strftime('%Y-%m-%d')
            
            # Build a list of dictionaries for each day containing "Date" and "Close"
            daily_data = []
            for date, row in hist.iterrows():
                daily_data.append({
                    "Date": date,
                    "Close": row["Close"]
                })
            
            # Store the data under a key representing the date range
            ticker_data[f"{start_date}_{end_date}"] = daily_data
            print(f"Fetched data for {ticker} from {start_date} to {end_date}")
            
            # Sleep to avoid potential rate limiting
            time.sleep(1)
            
        except Exception as e:
            print(f"Error fetching data for {ticker} ({start_date} to {end_date}): {e}")
    
    return ticker_data

def main():
    # Create a combined list of tickers from both US and foreign companies
    all_tickers = usCompanies + foreignCompanies
    
    # Process each ticker individually
    for ticker in all_tickers:
        print(f"\nProcessing ticker: {ticker}")
        data = fetch_ticker_data(ticker, date_ranges)
        
        # Save the data for each ticker into its own JSON file
        filename = f"{ticker}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data for {ticker} saved to {filename}")

if __name__ == "__main__":
    main()
