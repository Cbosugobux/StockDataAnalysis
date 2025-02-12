import yfinance as yf
import json
import time

# Define the companies (you can combine US and foreign companies into one list)
usCompanies = ["AAPL", "NVDA", "MSFT", "AMZN", "GOOG", "META", "TSLA", "AVGO", "ORCL", "CRM"]
foreignCompanies = ["TSM", "SSNLF", "ASML", "TCEHY", "BABA", "SAP", "SONY", "SOBKY", "INFY", "BIDU"]
all_tickers = usCompanies + foreignCompanies

# This list will hold the data for each company
market_cap_data = []

for ticker in all_tickers:
    print(f"Processing ticker: {ticker}")
    stock = yf.Ticker(ticker)
    
    try:
        # Fetch the info dictionary and extract the market capitalization.
        info = stock.info
        market_cap = info.get("marketCap")
        
        # Append a dictionary with just the ticker and marketCap.
        market_cap_data.append({
            "ticker": ticker,
            "marketCap": market_cap
        })
        
        print(f"Fetched market cap for {ticker}: {market_cap}")
        
    except Exception as e:
        print(f"Error fetching market cap for {ticker}: {e}")
    
    # Sleep briefly to avoid hitting API rate limits.
    time.sleep(1)

# Save the list of ticker-market cap dictionaries to a JSON file.
output_filename = "ticker_market_caps.json"
with open(output_filename, "w") as f:
    json.dump(market_cap_data, f, indent=4)

print(f"Data saved to {output_filename}")

