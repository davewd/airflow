__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import uuid
from ofxparse import OfxParser
import os
import pandas as pd
from collections import defaultdict


def convert_transactions_to_dataframes(objects, attribute_dict):
    # Dictionary to store objects sorted by class type
    class_dict = defaultdict(list)

    # Sort objects by class type
    for obj in objects:
        class_dict[obj.__class__.__name__].append(obj)

    # Convert each list of objects to a DataFrame
    dataframes = {}
    for class_name, objs in class_dict.items():
        df = pd.DataFrame([{**obj.__dict__, **attribute_dict} for obj in objs])
        dataframes[class_name] = df

    # add currency info.

    return dataframes


def convert_ofx_file_to_dataframes(ofx_file):

    if len(ofx_file.accounts) != 1:
        raise ValueError("OFX file must contain exactly one account")

    for account in ofx_file.accounts:
        txns = account.statement.transactions
        attribute_dict = account.to_dict()
        dataframes = convert_transactions_to_dataframes(txns, attribute_dict)

    return dataframes


def main():
    path = "/Users/daviddawson/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/airflow/adhoc_data/FY2023"
    os.chdir(path)

    # IDentify and iterate through all file names in the path location
    file_names = os.listdir()

    for file_name in file_names:
        if file_name.endswith(".ofx"):
            # file_name = "U8167557_20230703_20240628.ofx"
            # Open the file:
            with open(file_name, "rb") as fileobj:
                ofx_file = OfxParser.parse(fileobj)

            dataframes = convert_ofx_file_to_dataframes(ofx_file)
            _keys = dataframes.keys()
            for _key in _keys:
                dataframes[_key]


if __name__ == "__main__":
    main()
