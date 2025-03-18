__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import logging
import sys

# Configure root logger to send logs to stdout
logging.basicConfig(level=logging.INFO, stream=sys.stdout)
logger = logging.getLogger(__name__)
logger.info("Runner Logging Initiated")

import argparse
import datetime
import importlib

import dynamic_import_lib

logger.info("Dynamic Importer Initiated")


def main(args):
    arg_module = args.jobModule
    run_datetime = args.runDate
    log_level = args.logLevel

    logger.info(f"Starting Module: {arg_module} for run Date/Time: {run_datetime} logging level: {log_level}")
    logger.info(f"Sys Metapath currently looks like: {sys.meta_path}")
    is_docker = dynamic_import_lib.is_running_in_docker()
    logger.info(f"Docker Fn evaluated {is_docker} and uri : {dynamic_import_lib._db_uri}")

    if log_level == "ERROR":
        logger.setLevel(logging.ERROR)
    elif log_level == "DEBUG":
        logger.setLevel(logging.DEBUG)
    elif log_level == "INFO":
        logger.setLevel(logging.INFO)
    else:
        logger.setLevel(logging.ERROR)


    arg_module = fullname = "jobs.market_data.ecb.fx_api"
    arg_module_import = importlib.import_module(arg_module, "...")
    arg_module_import.main(args)
    # Your code to use the runtime argument goes here


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Parse arguments to injection into python layer")
    parser.add_argument(
        "--jobModule",
        "-j",
        default="jobs.market_data.ecb.fx_api",
        type=str,
        required=True,
    )
    parser.add_argument("--runDate", "-d", default=datetime.date(2024, 1, 1), type=str, required=True)
    parser.add_argument("--logLevel", "-l", default="ERROR", type=str, required=False)
    args = parser.parse_args()
    main(args)

# https://stackoverflow.com/questions/72395188/how-to-dynamically-import-module-from-a-relative-path-with-python-importlib
