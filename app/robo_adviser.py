import csv
from dotenv import load_dotenv
import json
import os
import pdb
import requests
#from IPython import embed

def parse_response(response_text):
    if isinstance(response_text, str):
        response_text = json.loads(response_text)

    results = []
    time_series_daily = response_text["Time Series (Daily)"]
    for trading_date in time_series_daily:
        prices = time_series_daily[trading_date]
        result = {
            "date": trading_date,
            "open": prices["1. open"],
            "high": prices["2. high"],
            "low": prices["3. low"],
            "close": prices["4. close"],
            "volume": prices["5. volume"]
        }
        results.append(result)
    return results

def write_prices_to_file(prices=[], filename="db/prices.csv"):
    csv_filepath = os.path.join(os.path.dirname(__file__), "..", filename)
    with open(csv_filepath, "w") as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=["timestamp", "open", "high", "low", "close", "volume"])
        writer.writeheader()
        for d in prices:
            row = {
                "timestamp": d["date"],
                "open": d["open"],
                "high": d["high"],
                "low": d["low"],
                "close": d["close"],
                "volume": d["volume"]
            }
            writer.writerow(row)

if __name__=='__main__':

    load_dotenv() # loads environment variables set in a ".env" file, including the value of the ALPHAVANTAGE_API_KEY variable

    # see: https://www.alphavantage.co/support/#api-key
    api_key = os.environ.get("ALPHAVANTAGE_API_KEY") or "OOPS. Please set an environment variable named 'ALPHAVANTAGE_API_KEY'."

    #symbol = "NFLX" #TODO: capture user input
    symbol = input("Please input a stock symbol (e.g. 'NFLX'):  ")

    #converted_symbool = float(symbol)
    #if isinstance(converted_symbool, float):
    #    print("CHECK YOUR SYMBOL. EXPECTING A NON-NUMERIC SYMBOL")
    #    quit()

    try:
        float(symbol)
        quit("CHECK YOUR SYMBOL. EXPECTING A NON-NUMERIC SYMBOL")
    except ValueError as e:
        pass

    # see: https://www.alphavantage.co/documentation/#daily
    # TODO: assemble the request url to get daily data for the given stock symbol
    request_url = f"https://www.alphavantage.co/query?function=TIME_SERIES_DAILY&symbol={symbol}&apikey={api_key}"

    response = requests.get(request_url)

    if "Error Message" in response.text:
        print ("REQUEST ERROR, PLEASE TRY AGAIN. CHECK YOUR STOCK SYMBOL.")
        quit("Stopping the program")


    daily_prices = parse_response(response.text)

    write_prices_to_file(prices=daily_prices, filename="db/prices.csv")

# TODO: traverse the nested response data structure to find the latest closing price
#metadata = response_body["Meta Data"]
#data = response_body["Time Series (Daily)"]
#dates = list(data)
#latest_daily_data = data[dates[1]]
#print(dates)
#
#print(f"LATEST DAILY CLOSING PRICE FOR {symbol} IS: {latest_price_usd}")
#
