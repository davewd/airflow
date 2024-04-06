__author__ = "David Dawson"
__copyright__ = "Copyright 2020, David Dawson"
__credits__ = ["David Dawson"]
__license__ = "GPL"
__version__ = "1.0.1"
__maintainer__ = "Dave Dawson"
__email__ = "davedawson.co@gmail.com"
__status__ = "Production"

import sys
import pymongo
import importlib.util
import logging

logger = logging.getLogger(__name__)
from urllib.parse import quote_plus


class MongoDBModuleLoader(importlib.abc.Loader):
    def __init__(self, db_uri, db_name, collection_name):
        self.client = pymongo.MongoClient(db_uri)
        self.db = self.client[db_name]
        self.collection = self.db[collection_name]

    def load_module(self, module_name):
        module_data = self.collection.find_one({"_id": module_name})

        if module_data is None:
            # This is a package
            _related_modules_and_sub_packages = [
                doc["_id"] for doc in self.collection.find({"_id": {"$regex": f".*{module_name}\..*"}})
            ]  # should this alllow .* prior to the module name ?
            # Create a set to store unique prefixes
            prefixes = set()

            # Iterate over each module name in the list
            for name in _related_modules_and_sub_packages:
                # Split the module name at '.' delimiter
                parts = name.split(".")

                # Iterate over each part of the module name
                for i in range(1, len(parts)):
                    # Join the parts up to the current index and add it to the set
                    prefix = ".".join(parts[2:i])
                    if len(prefix):
                        prefixes.add(prefix)

            # Convert the set to a sorted list
            result = sorted(prefixes)
            all_list = '", "'.join(result)
            module_data = {"content": f'__all__=[ "{all_list}"]'}  # manually construct the list of sub packages and modules

        if module_data:
            module_code = module_data.get("content", "")
            module = self._create_module(module_name, module_code)
            return module
        else:
            logger.info(f"Failed for {module_name}")
            raise ImportError(f"Module '{module_name}' not found in MongoDB collection.")

    def _create_module(self, module_name, module_code):
        spec = importlib.util.spec_from_loader(module_name, loader=None)
        module = importlib.util.module_from_spec(spec)
        self._exec_module(module, module_code)

        # Handle nested packages
        package_path = module_name.split(".")
        parent_package = ".".join(package_path[:-1])
        if parent_package:
            if parent_package not in sys.modules:
                self.load_module(parent_package)
            setattr(sys.modules[parent_package], package_path[-1], module)

        sys.modules[module_name] = module  # Cache the module in sys.modules
        return module

    def _exec_module(self, module, module_code):
        try:
            _ = sys.modules.pop(module.__name__)
        except KeyError:
            logger.error("module %s is not in sys.modules", module.__name__)
            # Create a new module object if it doesn't exist

        if not hasattr(module, "__file__"):
            module.__file__ = module.__name__

        # Execute module code in the module's namespace
        exec(module_code, module.__dict__)

        sys.modules[module.__name__] = module
        globals()[module.__name__] = module


class MongoDBImporter:
    def __init__(self, db_uri, db_name, collection_name):
        self.loader = MongoDBModuleLoader(db_uri, db_name, collection_name)

    def find_spec(self, fullname, path, target=None):
        if fullname not in sys.modules:  # Check if the module is not already imported
            return importlib.util.spec_from_loader(fullname, loader=self.loader)


username = "dd_python_codebase_down"
password = "download_me"
uri = "mongodb://%s:%s@localhost:27017/" % (
    quote_plus(username),
    quote_plus(password),
)

# Insert our MongoDBImporter into sys.meta_path
sys.meta_path.insert(0, MongoDBImporter(uri, "dwdrun", "codebase"))

# Example usage:
if __name__ == "__main__":
    try:
        import data_aquisition
        import data_aquisition.market_data.ecb.fx_api

        module_name = input("Enter module name to import from MongoDB: ")
        module = __import__(module_name)
        print(f"Module '{module_name}' imported successfully from MongoDB.")
        # You can now use the module as usual
    except ImportError as e:
        print(e)


_aa = 123
