__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import datetime
import argparse
import importlib


def main(args):
    arg_module = args.jobModule
    arg_module_import = importlib.import_module(arg_module)
    arg_module_import.main(args)
    # Your code to use the runtime argument goes here


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Parse arguments to injection into python layer"
    )
    parser.add_argument(
        "--jobModule",
        "-j",
        default="python_codebase.data_aquisition.market_data.ecb.fx_api",
        type=str,
        required=True,
    )
    parser.add_argument(
        "--runDate", "-d", default=datetime.date(2024, 1, 1), type=str, required=True
    )
    args = parser.parse_args()
    main(args)
