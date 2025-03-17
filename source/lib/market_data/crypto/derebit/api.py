__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"


api_name = "personal_ro"

import requests
import json
from datetime import datetime, timedelta

def download_historical_option_data(instrument_name, start_timestamp, end_timestamp):
    url = "https://www.deribit.com/api/v2/public/get_last_trades_by_instrument"
    params = {
        "instrument_name": instrument_name,
        "start_timestamp": start_timestamp,
        "end_timestamp": end_timestamp,
        "count": 1000,  # Maximum number of trades to retrieve per request
        "include_old": True  # Include old trades
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        historical_data = response.json()
        return historical_data

    except requests.exceptions.RequestException as e:
        print(f"Error fetching historical option data: {e}")
        return None

def main():
    # Define instrument name for the option you want historical data for
    instrument_name = "BTC-28MAY21-32000-C"  # Example instrument name

    # Define start and end timestamps for the historical data range (in milliseconds)
    end_timestamp = int(datetime.now().timestamp()) * 1000  # Current timestamp
    start_timestamp = end_timestamp - (86400 * 1000)  # 86400 seconds = 1 day

    historical_data = download_historical_option_data(instrument_name, start_timestamp, end_timestamp)

    if historical_data:
        print("Historical Option Data:")
        print(json.dumps(historical_data, indent=4))
    else:
        print("Failed to download historical option data.")





import pandas as pd
import requests
import json
from pivottablejs import pivot_ui
import tempfile


    tf = tempfile.NamedTemporaryFile(prefix="sho_", suffix=".html", delete=False)
    file_path = tf.name
    cols = list(df
    .columns.values)
    print(f"File Name : {tf.name}")
    pivot_ui(df, outfile_path=file_path, rows=cols)


def download_option_pricing_matrix():
    url = "https://www.deribit.com/api/v2/public/get_book_summary_by_currency"
    params = {"currency": "BTC", "kind": "option"}

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes

        option_pricing_matrix = response.json()
        
        df = pd.DataFrame(option_pricing_matrix["result"])
       
        # Define a regular expression pattern to match the date pattern
        date_pattern = r"(\d+)(\w{3})(\d{2})-(\d+)-(\w)"

        # Extract date components from each string in the Instrument_name column
        dates = df['instrument_name'].str.extract(date_pattern)

        # Rename the columns
        dates.columns = ["Day", "Month", "Year", "Numeric", "Put_Call"]

        # Map month abbreviations to month names
        month_mapping = {
            "JAN": "January",
            "FEB": "February",
            "MAR": "March",
            "APR": "April",
            "MAY": "May",
            "JUN": "June",
            "JUL": "July",
            "AUG": "August",
            "SEP": "September",
            "OCT": "October",
            "NOV": "November",
            "DEC": "December"
        }

        # Replace month abbreviations with month names
        dates["Month"] = dates["Month"].map(month_mapping)

        # Convert year to full year format (assuming 2-digit years belong to the 21st century)
        dates["Year"] = "20" + dates["Year"]

         # Split 'Day' column into two separate columns: 'DayNumeric' and 'DaySuffix'
        dates[['DayNumeric', 'DaySuffix']] = dates['Day'].str.extract(r'(\d+)(st|nd|rd|th)')

        
        # Convert date components to datetime format
        dates["Date"] = pd.to_datetime(dates["Day"] + dates["Month"] + dates["Year"], format='%d%B%Y')


        # Concatenate the dates DataFrame with the original DataFrame
        df_with_dates = pd.concat([df, dates], axis=1)

        tf = tempfile.NamedTemporaryFile(prefix="sho_", suffix=".html", delete=False)
        file_path = tf.name
        cols = list(df.columns.values)
        
        print(f"File Name : {tf.name}")
        pivot_ui(df_with_dates, outfile_path=file_path, rows=cols)

        return df_with_dates

    except requests.exceptions.RequestException as e:
        print(f"Error fetching option pricing matrix: {e}")
        return None


def main():
    option_pricing_matrix = download_option_pricing_matrix()

    if option_pricing_matrix:
        print("Option Pricing Matrix:")
        print(json.dumps(option_pricing_matrix, indent=4))
    else:
        print("Failed to download option pricing matrix.")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    main()
