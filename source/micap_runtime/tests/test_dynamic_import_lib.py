"""Tests for the dynamic_import_lib module."""
import sys
from collections.abc import Generator
from unittest.mock import MagicMock, patch

import pytest

from ..dynamic_import_lib import MongoDBImporter, MongoDBModuleLoader


@pytest.fixture
def mock_mongo_client() -> Generator[MagicMock, None, None]:
    """Create a mock MongoDB client for testing.

    Returns:
        Generator yielding a mock collection object for testing MongoDB operations.
    """
    with patch('pymongo.MongoClient') as mock_client:
        mock_collection = MagicMock()
        mock_db = MagicMock()
        mock_db.__getitem__.return_value = mock_collection
        mock_client.return_value.__getitem__.return_value = mock_db
        yield mock_collection


@pytest.fixture
def module_loader(mock_mongo_client: MagicMock) -> MongoDBModuleLoader:
    """Create a MongoDBModuleLoader instance with mocked MongoDB client.

    Args:
        mock_mongo_client: Mocked MongoDB collection.

    Returns:
        Configured MongoDBModuleLoader instance.
    """
    with patch('pymongo.MongoClient'):
        loader = MongoDBModuleLoader()
        loader.collection = mock_mongo_client
        return loader


@pytest.fixture
def module_importer(module_loader: MongoDBModuleLoader) -> MongoDBImporter:
    """Create a MongoDBImporter instance with mocked loader.

    Args:
        module_loader: Mocked MongoDBModuleLoader instance.

    Returns:
        Configured MongoDBImporter instance.
    """
    importer = MongoDBImporter()
    importer.loader = module_loader
    return importer


def test_get_data_success(module_loader: MongoDBModuleLoader) -> None:
    """Test successful retrieval of module data from MongoDB."""
    expected_content = "def test_function(): return 'Hello'"
    module_loader.collection.find_one.return_value = {
        "_id": "test.module",
        "content": expected_content
    }

    result = module_loader.get_data("test.module")

    assert result == expected_content
    module_loader.collection.find_one.assert_called_once_with(
        {"_id": "test.module"},
        max_time_ms=1000
    )


def test_get_data_not_found(module_loader: MongoDBModuleLoader) -> None:
    """Test behavior when module data is not found in MongoDB."""
    module_loader.collection.find_one.return_value = None

    with pytest.raises(FileNotFoundError, match="Module test.module not found"):
        module_loader.get_data("test.module")


def test_get_sub_module_data(module_loader: MongoDBModuleLoader) -> None:
    """Test retrieval of submodule data from MongoDB."""
    mock_documents = [
        {"_id": "lib.logging.utils"},
        {"_id": "lib.logging.formatters"},
        {"_id": "lib.logging.handlers"}
    ]
    module_loader.collection.find.return_value = mock_documents

    result = module_loader.get_sub_module_data("lib.logging")

    # Check that __all__ is created correctly with direct children only
    assert result["content"] == '__all__ = ["formatters", "handlers", "utils"]'
    module_loader.collection.find.assert_called_once()


def test_get_sub_module_data_nested(module_loader: MongoDBModuleLoader) -> None:
    """Test retrieval of nested submodule data from MongoDB."""
    mock_documents = [
        {"_id": "lib.logging.utils"},
        {"_id": "lib.logging.utils.common"},
        {"_id": "lib.logging.formatters"},
        {"_id": "lib.logging.handlers.custom"}
    ]
    module_loader.collection.find.return_value = mock_documents

    result = module_loader.get_sub_module_data("lib.logging")

    # Should only include direct children: formatters, handlers, utils
    assert result["content"] == '__all__ = ["formatters", "handlers", "utils"]'


    mock_documents = [
        {"_id": "lib.logging.utils"},
        {"_id": "lib.logging.utils.common"},
    ]
    module_loader.collection.find.return_value = mock_documents

    # Test for a specific subpackage
    result = module_loader.get_sub_module_data("lib.logging.utils")
    assert result["content"] == '__all__ = ["common"]'


def test_exec_module_regular_module(module_loader: MongoDBModuleLoader) -> None:
    """Test execution of a regular module code retrieved from MongoDB."""
    mock_module = MagicMock()
    mock_module.__name__ = "test.module"
    mock_module.__dict__ = {}

    test_code = "def test_func(): return 42"
    module_loader.get_data = MagicMock(return_value=test_code)

    with patch.dict(sys.modules, {}, clear=True):
        module_loader.exec_module(mock_module)

    assert "test_func" in mock_module.__dict__
    assert mock_module.__dict__["test_func"]() == 42
    assert mock_module.__name__ in sys.modules


def test_exec_module_package(module_loader: MongoDBModuleLoader) -> None:
    """Test execution of a package module code retrieved from MongoDB."""
    mock_module = MagicMock()
    mock_module.__name__ = "test.package"
    mock_module.__dict__ = {}

    # Simulate FileNotFoundError for direct module, indicating it's a package
    module_loader.get_data = MagicMock(side_effect=FileNotFoundError("Module not found"))

    # Setup the package to have submodules
    mock_sub_modules = {'content': '__all__ = ["submodule1", "submodule2"]'}
    module_loader.get_sub_module_data = MagicMock(return_value=mock_sub_modules)

    # Mock the collection.count_documents to indicate submodules exist
    module_loader.collection.count_documents = MagicMock(return_value=2)

    with patch.dict(sys.modules, {}, clear=True):
        module_loader.exec_module(mock_module)

    # Check that __all__ was properly set
    assert "__all__" in mock_module.__dict__
    assert module_loader.get_sub_module_data.called
    assert hasattr(mock_module, "__path__")
    assert mock_module.__name__ in sys.modules


def test_find_spec_for_module(module_importer: MongoDBImporter) -> None:
    """Test finding module spec for a regular module."""
    # Setup module_loader to return data for a module
    module_importer.loader.get_data = MagicMock(return_value="module_content")

    with patch.dict(sys.modules, {}, clear=True):
        spec = module_importer.find_spec("test.module")

    assert spec is not None
    assert spec.name == "test.module"
    assert spec.loader == module_importer.loader
    assert spec.submodule_search_locations is None  # Not a package


def test_find_spec_for_package(module_importer: MongoDBImporter) -> None:
    """Test finding module spec for a package."""
    # Setup module_loader to fail for direct module but have submodules
    module_importer.loader.get_data = MagicMock(side_effect=FileNotFoundError)
    module_importer.loader.collection.count_documents = MagicMock(return_value=3)

    with patch.dict(sys.modules, {}, clear=True):
        spec = module_importer.find_spec("test.package")

    assert spec is not None
    assert spec.name == "test.package"
    assert spec.loader == module_importer.loader
    assert spec.submodule_search_locations is not None  # Is a package


def test_from_import_syntax(module_loader: MongoDBModuleLoader) -> None:
    """Test the 'from x import y' syntax with the MongoDB loader."""
    # Setup collection to return modules and submodules
    package_structure = {
        "lib": {"content": '__all__ = ["logging"]'},
        "lib.logging": {"content": '__all__ = ["utils"]'},
        "lib.logging.utils": {"content": 'DEFAULT_LOG_LEVEL = "INFO"\n\ndef setup_logging(level=DEFAULT_LOG_LEVEL):\n    return level'}
    }

    def mock_find_one(query, **kwargs):
        module_id = query.get("_id")
        if module_id in package_structure:
            return {"_id": module_id, **package_structure[module_id]}
        return None

    def mock_find(query, **kwargs):
        pattern = query["_id"]["$regex"]
        pattern = pattern[1:-1]  # Remove the ^$ wrapper
        results = []
        for key in package_structure:
            if key.startswith(pattern) and key != pattern:
                results.append({"_id": key})
        return results

    def mock_count_documents(query, **kwargs):
        pattern = query["_id"]["$regex"]
        pattern = pattern[1:-2]  # Remove the ^$ and \. wrapper
        count = 0
        for key in package_structure:
            if key.startswith(pattern + "."):
                count += 1
        return count

    module_loader.collection.find_one = MagicMock(side_effect=mock_find_one)
    module_loader.collection.find = MagicMock(side_effect=mock_find)
    module_loader.collection.count_documents = MagicMock(side_effect=mock_count_documents)

    importer = MongoDBImporter()
    importer.loader = module_loader

    # Make sure our modules aren't already loaded
    for mod in ["lib", "lib.logging", "lib.logging.utils"]:
        if mod in sys.modules:
            del sys.modules[mod]

    sys.meta_path.insert(0, importer)

    try:
        # Test the from ... import ... syntax
        from_import_code = "from lib.logging.utils import DEFAULT_LOG_LEVEL, setup_logging"
        local_vars = {}
        exec(from_import_code, {}, local_vars)

        assert "DEFAULT_LOG_LEVEL" in local_vars
        assert local_vars["DEFAULT_LOG_LEVEL"] == "INFO"
        assert "setup_logging" in local_vars
        assert local_vars["setup_logging"]() == "INFO"

        # Verify proper loading of each component in the import chain
        assert "lib" in sys.modules
        assert "lib.logging" in sys.modules
        assert "lib.logging.utils" in sys.modules

    finally:
        sys.meta_path.remove(importer)
        for mod in ["lib", "lib.logging", "lib.logging.utils"]:
            if mod in sys.modules:
                del sys.modules[mod]


def test_hierarchical_import(module_loader: MongoDBModuleLoader) -> None:
    """Test hierarchical import process (package with subpackages and modules)."""
    # Create a more complex package structure
    package_structure = {
        "jobs": {"is_package": True},
        "jobs.market_data": {"is_package": True},
        "jobs.market_data.ecb": {"is_package": True},
        "jobs.market_data.ecb.fx_api": {"content": "def get_rates(): return {'EUR': 1.0, 'USD': 1.1}\n\nBASE_CURRENCY = 'EUR'"},
        "jobs.market_data.ecb.utils": {"content": "def process_rates(rates): return {k: v * 1.01 for k, v in rates.items()}"},
        "jobs.market_data.ecb.constants": {"content": "API_URL = 'https://example.com/api'\nTIMEOUT = 30"}
    }

    def mock_find_one(query, **kwargs):
        module_id = query.get("_id")
        if module_id in package_structure:
            result = {"_id": module_id}
            if "content" in package_structure[module_id]:
                result["content"] = package_structure[module_id]["content"]
            return result
        return None

    def mock_find(query, **kwargs):
        pattern = query["_id"]["$regex"]
        pattern = pattern[1:-1]  # Remove the ^$ wrapper
        results = []
        for key in package_structure:
            if key.startswith(pattern) and key != pattern:
                results.append({"_id": key})
        return results

    def mock_count_documents(query, **kwargs):
        pattern = query["_id"]["$regex"]
        pattern = pattern[1:-2]  # Remove the ^$ and \. wrapper
        count = 0
        for key in package_structure:
            if key.startswith(pattern + "."):
                count += 1
        return count

    def mock_get_data(fullname):
        if fullname in package_structure and "content" in package_structure[fullname]:
            return package_structure[fullname]["content"]
        raise FileNotFoundError(f"Module {fullname} not found")

    module_loader.collection.find_one = MagicMock(side_effect=mock_find_one)
    module_loader.collection.find = MagicMock(side_effect=mock_find)
    module_loader.collection.count_documents = MagicMock(side_effect=mock_count_documents)
    module_loader.get_data = MagicMock(side_effect=mock_get_data)

    importer = MongoDBImporter()
    importer.loader = module_loader

    # Make sure relevant modules aren't already loaded
    for mod in list(sys.modules.keys()):
        if mod.startswith("jobs"):
            del sys.modules[mod]

    sys.meta_path.insert(0, importer)

    try:
        # Test importing a specific function from a deeply nested module
        import_code = "from jobs.market_data.ecb.fx_api import get_rates, BASE_CURRENCY"
        local_vars = {}
        exec(import_code, {}, local_vars)

        assert "get_rates" in local_vars
        assert "BASE_CURRENCY" in local_vars
        assert local_vars["BASE_CURRENCY"] == "EUR"
        assert local_vars["get_rates"]()["EUR"] == 1.0

        # Verify proper loading of each component in the import chain
        assert "jobs" in sys.modules
        assert "jobs.market_data" in sys.modules
        assert "jobs.market_data.ecb" in sys.modules
        assert "jobs.market_data.ecb.fx_api" in sys.modules

    finally:
        sys.meta_path.remove(importer)
        for mod in list(sys.modules.keys()):
            if mod.startswith("jobs"):
                del sys.modules[mod]
