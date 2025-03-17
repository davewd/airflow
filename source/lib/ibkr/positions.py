#!/usr/bin/env python3
"""
IBKR Positions Module

Created on: 2025-03-06
Author: David Dawson
Purpose: Handles position-related functionality for Interactive Brokers integration
"""

# Standard library imports
from typing import Dict, List, Optional, Any
from datetime import datetime
import time
import requests
import pandas as pd
import json
import os

# Local imports
from lib.logging.utils import setup_logging

# Configure logging
logger = setup_logging(module_name=__name__)

base_url = "https://api.ibkr.com/v1/api"
session = requests.Session()
api_token = ""


def get_positions(self, account_id=None):
    """
    Get all positions for an account
    If account_id is not provided, it will get positions for all accounts
    """
    # API endpoint for positions
    url = f"{self.base_url}/portfolio/accounts"

    if account_id:
        url = f"{self.base_url}/portfolio/{account_id}/positions"

    # Set up headers with authentication
    headers = {"Authorization": f"Bearer {self.api_token}", "Content-Type": "application/json"}

    try:
        # First get the list of accounts if account_id was not provided
        if not account_id:
            response = self.session.get(url, headers=headers)
            if response.status_code != 200:
                print(f"Error getting accounts: {response.status_code}")
                print(response.text)
                return []

            accounts = response.json()
            all_positions = []

            # For each account, get positions
            for account in accounts:
                account_id = account.get("id")
                print(f"Getting positions for account: {account_id}")

                positions_url = f"{self.base_url}/portfolio/{account_id}/positions"
                positions_response = self.session.get(positions_url, headers=headers)

                if positions_response.status_code == 200:
                    positions = positions_response.json()

                    # Add account ID to each position
                    for position in positions:
                        position["accountId"] = account_id
                        all_positions.append(position)
                else:
                    print(f"Error getting positions for account {account_id}: {positions_response.status_code}")
                    print(positions_response.text)

            return all_positions
        else:
            # Direct request for a specific account
            response = self.session.get(url, headers=headers)

            if response.status_code == 200:
                positions = response.json()

                # Add account ID to each position
                for position in positions:
                    position["accountId"] = account_id

                return positions
            else:
                print(f"Error getting positions: {response.status_code}")
                print(response.text)
                return []

    except Exception as e:
        print(f"Error: {str(e)}")
        return []


def format_positions(positions):
    """Format the positions into a DataFrame"""
    if not positions:
        return None

    formatted_positions = []
    for pos in positions:
        formatted_pos = {
            "Account": pos.get("accountId"),
            "Symbol": pos.get("contract", {}).get("symbol"),
            "SecType": pos.get("contract", {}).get("secType"),
            "Currency": pos.get("contract", {}).get("currency"),
            "Exchange": pos.get("contract", {}).get("exchange"),
            "Quantity": pos.get("position"),
            "MarketPrice": pos.get("marketPrice"),
            "MarketValue": pos.get("marketValue"),
            "AverageCost": pos.get("avgCost"),
            "UnrealizedPnL": pos.get("unrealizedPnL"),
            "RealizedPnL": pos.get("realizedPnL"),
        }
        formatted_positions.append(formatted_pos)

    return pd.DataFrame(formatted_positions)


def main():
    print("IBKR Position Tracker using REST API")
    print("====================================")

    # Create API client

    # Optional: Get specific account ID or leave as None for all accounts
    account_id = "U8167557"

    # Get positions
    print("\nRetrieving positions...")
    positions = get_positions(account_id)

    # Format and display positions
    if positions:
        df = format_positions(positions)
        print("\nYour positions:")
        print(df)

        # Save to CSV with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"ibkr_positions_{timestamp}.csv"
        df.to_csv(csv_filename, index=False)
        print(f"\nPositions saved to '{csv_filename}'")

        # Save raw data to JSON
        json_filename = f"ibkr_positions_raw_{timestamp}.json"
        with open(json_filename, "w") as f:
            json.dump(positions, f, indent=2)
        print(f"Raw position data saved to '{json_filename}'")
    else:
        print("No positions found or error retrieving positions.")


if __name__ == "__main__":
    main()
