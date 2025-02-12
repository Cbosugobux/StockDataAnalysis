import yfinance as yf
import json
import time

# Define the companies
usCompanies = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "META", "TSLA", "AVGO", "ORCL", "CRM"]
foreignCompanies = ["TSM", "SSNLF", "ASML", "TCEHY", "BABA", "SAP", "SONY", "SOBKY", "INFY", "BIDU"]

# Define the presidential term date ranges
presidential_terms = {
    "Trump": ("2017-01-20", "2017-12-31"),
    "Biden": ("2021-01-20", "2021-12-31")
}

def fetch_ticker_data(ticker, start_date, end_date):
    """
    Fetch historical stock data for the given ticker between start_date and end_date.
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
    Fetch company name, market cap, and address from Yahoo Finance.
    Returns a dictionary with company details.
    """
    stock = yf.Ticker(ticker)
    try:
        info = stock.info
        company_name = info.get("shortName", ticker)
        market_cap = info.get("marketCap", "N/A")
        address = {
            "Street": info.get("address1", "N/A"),
            "City": info.get("city", "N/A"),
            "State": info.get("state", "N/A"),
            "Zip": info.get("zip", "N/A"),
            "Country": info.get("country", "N/A")
        }
        return company_name, market_cap, address
    except Exception as e:
        print(f"Error retrieving info for {ticker}: {e}")
        return ticker, "N/A", {}

def main():
    all_tickers = usCompanies + foreignCompanies

    # Initialize dictionaries to hold data for each president
    data_by_president = {president: {} for president in presidential_terms}

    for ticker in all_tickers:
        print(f"\nProcessing ticker: {ticker}")
        company_name, market_cap, address = fetch_company_info(ticker)

        for president, (start_date, end_date) in presidential_terms.items():
            print(f"Fetching data for {company_name} ({ticker}) during {president}'s term ({start_date} to {end_date})")
            historical_data = fetch_ticker_data(ticker, start_date, end_date)

            if historical_data:
                if company_name not in data_by_president[president]:
                    data_by_president[president][company_name] = {
                        "Market Cap": market_cap,
                        "Address": address
                    }
                data_by_president[president][company_name][f"{start_date}_{end_date}"] = historical_data
            
            time.sleep(1)  # Sleep to avoid rate limiting

    # Save data to JSON files
    for president, data in data_by_president.items():
        filename = f"{president}.json"
        with open(filename, "w") as f:
            json.dump(data, f, indent=4)
        print(f"Data saved to {filename}")

if __name__ == "__main__":
    main()
