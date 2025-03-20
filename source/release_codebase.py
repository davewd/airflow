#!/usr/bin/env python3
"""MongoDB Python Module Release Tool
--------------------------------
Purpose:
    Traverses a directory structure and uploads Python modules to MongoDB,
    maintaining proper package hierarchy and automatically managing __init__.py files.

Created: 2025-03-20
Author: David Dawson
License: GPL
"""

__author__ = "David Dawson"
__copyright__ = "Copyright 2025, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import logging
import os
from urllib.parse import quote_plus

from lib.logging.utils import setup_logging
from pymongo import MongoClient

logger = setup_logging(level=logging.INFO, module_name="release_codebase")
init_hierarchy = {}

# Replace 'your_username' and 'your_password' with your actual username and password
username = "dd_python_codebase"
password = "upload_me"
# Construct MongoDB connection string with username and password
uri = f"mongodb://{quote_plus(username)}:{quote_plus(password)}@localhost:27017/dwdrun?authSource=admin&retryWrites=true&w=majority"
client = MongoClient(uri)
db = client["dwdrun"]  # Replace 'your_database' with your actual database name
collection = db["codebase"]  # Replace 'your_collection' with your actual collection name

def traverse_directory(directory: str) -> None:
    """Traverse a directory and upload Python modules to MongoDB.

    This function walks through the directory structure, processes Python files,
    and ensures proper package hierarchy by managing __init__.py files.

    Args:
        directory: Root directory path to traverse.

    Returns:
        None
    """
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith(".py"): # TODO: make this work for all files e.g. readme or configs
                file_path = os.path.join(root, file)
                with open(file_path) as f:
                    content = f.read()
                    relative_file_path = os.path.relpath(file_path, directory)
                    for part in os.path.pathsep.split(relative_file_path):
                        if init_hierarchy.get(part, False):
                            #upsert_document(part, "__init__.py")
                            logger.info(f"Upserted document {part} into MongoDB")
                            init_hierarchy[part] = True

                    upsert_document(relative_file_path, content)

def upsert_document(relative_file_path: str, content: str) -> None:
    """Upload a Python module to MongoDB with proper hierarchy handling.

    This function processes the file path to create appropriate MongoDB records,
    handling special cases like __init__.py files and maintaining proper
    package structure.

    Args:
        relative_file_path: Path to the file relative to project root.
        content: Content of the Python file.

    Returns:
        None
    """
    record_name = relative_file_path.replace("/", ".")

    if record_name.endswith("__init__.py"):
        record_name = record_name[:-12]  # Remove '.__init__.py' from the end

    if record_name.endswith(".py"):
        record_name = record_name[:-3]  # Remove '.py' from the end

    # Upsert content into MongoDB collection
    collection.update_one({"_id": record_name}, {"$set": {"content": content}}, upsert=True)
    logger.info(f"Upserted document {record_name} into MongoDB")

def clear_collection() -> None:
    """Clear all documents from the MongoDB collection.

    This function removes all documents from the codebase collection and
    resets the hierarchy tracking.

    Returns:
        None
    """
    collection.delete_many({})
    logger.info("Collection cleared")

def main() -> None:
    """Main entry point of the script.

    Processes the source directory and uploads all Python modules to MongoDB.
    The source directory path is hardcoded for the current project structure.

    Returns:
        None
    """
    directory_path = "/Users/daviddawson/Library/Mobile Documents/com~apple~CloudDocs/Documents/projects/mi_capital/source"
    traverse_directory(directory_path)
    # Uncomment the line below to clear the collection (use with caution)
    # clear_collection()

if __name__ == "__main__":
    main()
