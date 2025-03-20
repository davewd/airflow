"""Main entry point for running MI Capital jobs and modules.

Handles dynamic module imports and execution with configurable logging.
Provides a command-line interface for executing various job modules with
customizable runtime parameters and logging configuration.

Created: 2025-03-20
"""

__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import argparse
import datetime
import importlib
import logging
import sys

import dynamic_import_lib
from lib.logging.utils import DEFAULT_LOG_LEVEL, setup_logging

# Initialize logger using the centralized logging utility
logger = setup_logging(module_name=__name__, level=DEFAULT_LOG_LEVEL)
logger.info("Runner Logging Initiated")
logger.info("Dynamic Importer Initiated")


def main(args: argparse.Namespace) -> None:
    """Execute the specified job module with given parameters.

    Args:
        args: Command line arguments containing jobModule, runDate, and logLevel.
    """
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
