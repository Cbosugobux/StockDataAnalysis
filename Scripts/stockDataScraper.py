import yfinance as yf
import json
import time

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

def main():
    all_tickers = usCompanies + foreignCompanies
    data_by_president = {"Trump": [], "Biden": []}  # Store data as lists for clarity

    for ticker in all_tickers:
        print(f"\nProcessing ticker: {ticker}")
        stock = yf.Ticker(ticker)
        try:
            company_name = stock.info.get("shortName", ticker)
        except Exception as e:
            print(f"Error retrieving name for {ticker}: {e}")
            company_name = ticker

        for president, (start_date, end_date) in date_ranges.items():
            print(f"Fetching data for {company_name} ({ticker}) during {president}'s term ({start_date} to {end_date})")
            historical_data = fetch_ticker_data(ticker, start_date, end_date)

            if historical_data:
                data_by_president[president].append({
                    "Ticker": ticker,
                    "Company Name": company_name,
                    "Date Range": f"{start_date} to {end_date}",
                    "Stock Data": historical_data
                })
            
            time.sleep(1)  # Sleep to avoid rate limiting

    # Save data to JSON files
    for president, data in data_by_president.items():
        filename = f"{president}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
