__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import _frozen_importlib
import importlib.util
import logging
import os
import re
import sys

import pymongo


def is_running_in_docker():
    """Check if the current environment is running inside a Docker container."""
    return os.environ.get("DOCKER_CONTAINER") == "true"


logger = logging.getLogger(__name__)
from urllib.parse import quote_plus

# TODO: Hide Credentials
_username = "dd_python_codebase_down"
_password = "download_me"
_hostname = "mongodb" if is_running_in_docker() else "localhost"
logger.info(f"is_running_in_docker: {is_running_in_docker()} as {_hostname}")
_db_uri = "mongodb://%s:%s@%s:27017/" % (quote_plus(_username), quote_plus(_password), _hostname)
_db_name = "dwdrun"
_collection_name = "codebase"


class MongoDBModuleLoader:

    def __init__(self):
        """Initialize the MongoDBModuleLoader with a connection to the codebase collection."""
        self.client = pymongo.MongoClient(_db_uri, waitQueueTimeoutMS=1000)
        self.db = self.client[_db_name]
        self.collection = self.db[_collection_name]
        logger.debug("Connected successfully to python codebase in mongo")

    def create_module(self, spec):
        """Create an uninitialized extension module"""
        # module = importlib.util.module_from_spec(spec)
        # self._exec_module(module, module_code)
        new_module = _frozen_importlib._new_module(spec.name)
        # new_module.__getattr__ = self.get_sub_modules
        new_module.__path__ = self.get_filename(spec.name)
        return new_module

    def get_sub_module_data(self, fullname):
        """Given a full name assume package and return all underlying sub modules"""
        pattern = f"^{re.escape(fullname)}\\."
        modules = [doc["_id"] for doc in self.collection.find({"_id": {"$regex": pattern}})]

        # Find direct children only
        direct_children = set()
        for module_name in modules:
            # Remove the package prefix
            relative_name = module_name[len(fullname)+1:]
            # Get only the first segment (direct child)
            first_segment = relative_name.split('.')[0]
            direct_children.add(first_segment)

        all_list = '", "'.join(sorted(direct_children))
        module_data = {"content": f'__all__ = ["{all_list}"]' if all_list else '__all__ = []'}
        return module_data

    def exec_module(self, module):
        """Initialize an extension module"""
        fullname = module.__name__

        try:
            # Try to get module code directly
            module_code = self.get_data(fullname)
            is_package = False
        except FileNotFoundError:
            # If not found, it might be a package
            pattern = f"^{re.escape(fullname)}\\."
            if self.loader.collection.count_documents({"_id": {"$regex": pattern}}) > 0:
                module_code = self.get_sub_module_data(fullname)
                is_package = True
            else:
                raise ImportError(f"Module '{fullname}' not found in MongoDB collection.")

        if not hasattr(module, "__file__"):
            module.__file__ = f"<mongodb>/{fullname.replace('.', '/')}"

        if is_package and not hasattr(module, "__path__"):
            module.__path__ = [fullname]

        # Execute module code in the module's namespace
        exec(module_code["content"], module.__dict__)

        # Ensure the module is in sys.modules
        sys.modules[fullname] = module

    def load_module(self, fullname):
        pass

    def get_data(self, fullname):
        record = self.collection.find_one({"_id": fullname}, max_time_ms=1000)
        if not record:
            raise FileNotFoundError(f"Module {fullname} not found")
        return record["content"]

    def get_filename(self, fullname):
        """Return the path to the source file as found by the finder."""
        record = self.collection.find_one({"_id": fullname}, max_time_ms=1000)
        if not record:
            raise FileNotFoundError(f"Module {fullname} not found")
        return record["_id"]


class MongoDBImporter:
    def __init__(
        self,
    ):
        self.loader = MongoDBModuleLoader()

    def find_spec(self, fullname, path=None, target=None):
        if fullname not in sys.modules:  # Check if the module is not already imported
            try:
                # Check if this is a direct module
                try:
                    self.loader.get_data(fullname)
                    return importlib.util.spec_from_loader(fullname, loader=self.loader, is_package=False)
                except FileNotFoundError:
                    # Check if this is a package (has submodules)
                    pattern = f"^{re.escape(fullname)}\\."
                    if self.loader.collection.count_documents({"_id": {"$regex": pattern}}) > 0:
                        return importlib.util.spec_from_loader(fullname, loader=self.loader, is_package=True)
                    return None
            except Exception as e:
                logger.debug(f"Failed importing from Mongo: {fullname}, error: {e}")
                return None
        return None


def setup_micap_importing() -> None:
    """Setup the MongoDB importer for dynamic module loading."""
    # Insert our MongoDBImporter into sys.meta_path
    sys.meta_path.insert(2, MongoDBImporter())
    logger.info("Added Dynamic libary to positon 2")

if __name__ == "__main__":
    setup_micap_importing()
