import yfinance as yf
import json
import time
import random

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

    # Store all tickers inside a single document (like Biden)
    for president, data in data_by_president.items():
        filename = f"{president}.json"
        with open(filename, "w") as f:
            json.dump([data], f, indent=4)  # Store as a list with one big dictionary
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
